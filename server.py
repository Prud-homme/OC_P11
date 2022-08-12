import json
from datetime import datetime
from math import floor

from flask import Flask, flash, redirect, render_template, request, url_for
from flask import Response


POINTS_PER_PLACE = 3


def load_clubs() -> list:
    """Extract the list of clubs from the json file"""
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions() -> list:
    """Extract the list of competitions from the json file"""
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = load_competitions()
clubs = load_clubs()


@app.route("/")
def index() -> Response:
    """Route for home page with login form"""
    return render_template("index.html")


@app.route("/show_summary", methods=["POST"])
def show_summary() -> Response:
    """
    Route to connect to the application
    and be redirected to the summary if successful
    """
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
    except IndexError:
        flash("Sorry, that email wasn't found.")
        return render_template("index.html")

    return render_template("welcome.html", club=club, competitions=competitions)


@app.template_filter("can_booking")
def can_booking_filter(competition: str) -> bool:
    """Checks if a date is after today and returns a boolean"""
    now = datetime.now()
    date_time = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    return date_time > now


@app.route("/book/<competition>/<club>")
def book(competition: str, club: str) -> Response:
    """
    If a club and a competition are found,
    the route redirecting to the purchase places form.
    Otherwise we return to the summary.
    """
    found_club = [c for c in clubs if c["name"] == club][0]

    try:
        found_competition = [c for c in competitions if c["name"] == competition][0]
    except IndexError:
        found_competition = None

    if found_club and found_competition and can_booking_filter(found_competition):
        return render_template(
            "booking.html", club=found_club, competition=found_competition
        )

    elif found_club and found_competition and not can_booking_filter(found_competition):
        flash("You cannot book places for an ended competition!")
        return render_template(
            "welcome.html", club=found_club, competitions=competitions
        )

    else:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html", club=found_club, competitions=competitions
        )


@app.route("/purchase_places", methods=["POST"])
def purchase_places() -> Response:
    """
    Route for purchase places of a competition
    Check if the required places are valid (>0, <12 and cost points)
    """
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    places_required = int(request.form["places"])
    max_places_can_book = floor(int(club["points"]) / POINTS_PER_PLACE)

    if not can_booking_filter(competition):
        flash("You cannot book places for an ended competition!")
        return render_template("welcome.html", club=club, competitions=competitions)

    elif places_required > 12:
        flash("Cannot booking more than 12 places per competition")
        return redirect(
            url_for("book", club=club["name"], competition=competition["name"])
        )

    elif places_required < 0:
        flash("Cannot booking less than 0 place per competition")
        return redirect(
            url_for("book", club=club["name"], competition=competition["name"])
        )

    elif places_required > max_places_can_book:
        flash(f"You cannot book more than {max_places_can_book} places")
        return redirect(
            url_for("book", competition=competition["name"], club=club["name"])
        )

    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - places_required
    club["points"] = int(club["points"]) - places_required * POINTS_PER_PLACE
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/clubs_points")
def clubs_points() -> Response:
    """Route displaying a table of clubs and their points"""
    return render_template("board_clubs_points.html", clubs=clubs)


@app.route("/logout")
def logout() -> Response:
    """Route for logout to the app"""
    flash("Successful logout!")
    return redirect(url_for("index"))
