import json
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for


def load_clubs():
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions():
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = load_competitions()
clubs = load_clubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/show_summary", methods=["POST"])
def show_summary():
    club = [club for club in clubs if club["email"] == request.form["email"]][0]
    return render_template("welcome.html", club=club, competitions=competitions)


@app.template_filter("can_booking")
def can_booking_filter(competition):
    now = datetime.now()
    date_time = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    return date_time > now


@app.route("/book/<competition>/<club>")
def book(competition, club):
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
def purchase_places():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    places_required = int(request.form["places"])

    if not can_booking_filter(competition):
        flash("You cannot book places for an ended competition!")
        return render_template("welcome.html", club=club, competitions=competitions)

    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - places_required
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
