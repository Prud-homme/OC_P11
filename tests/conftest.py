from datetime import datetime, timedelta

import pytest

import server


@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client


def generate_future_competitions():
    """Generates a list of competitions with a date after today"""
    now = datetime.now()
    datetime1 = now + timedelta(days=10)
    datetime2 = now + timedelta(days=50)
    datetime3 = now + timedelta(days=365)
    datetime4 = now + timedelta(days=800)
    competitions = [
        {
            "name": "Spring Festival",
            "date": datetime1.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "24",
        },
        {
            "name": "Fall Classic",
            "date": datetime2.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "12",
        },
        {
            "name": "Spring Classic",
            "date": datetime3.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "7",
        },
        {
            "name": "Summer Festival",
            "date": datetime4.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "0",
        },
    ]
    return competitions


@pytest.fixture
def mocker_future_competitions(mocker):
    mocker.patch.object(server, "competitions", generate_future_competitions())


def generate_past_competitions():
    """Generates a list of competitions with a date before today"""
    now = datetime.now()
    datetime1 = now - timedelta(days=10)
    datetime2 = now - timedelta(days=50)
    datetime3 = now - timedelta(days=365)
    datetime4 = now - timedelta(days=800)
    competitions = [
        {
            "name": "Spring Festival",
            "date": datetime1.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "24",
        },
        {
            "name": "Fall Classic",
            "date": datetime2.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "12",
        },
        {
            "name": "Spring Classic",
            "date": datetime3.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "7",
        },
        {
            "name": "Summer Festival",
            "date": datetime4.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "0",
        },
    ]
    return competitions


@pytest.fixture
def mocker_past_competitions(mocker):
    mocker.patch.object(server, "competitions", generate_past_competitions())


def generate_clubs():
    """Generates a list of clubs"""
    clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": str(15 * server.POINTS_PER_PLACE),
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": str(5 * server.POINTS_PER_PLACE),
        },
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "0"},
    ]
    return clubs


@pytest.fixture
def mocker_clubs(mocker):
    mocker.patch.object(server, "clubs", generate_clubs())


def generate_valid_purchase():
    """
    Return a tuple containing tuples.
    Each of these tuples represents a club and
    a number of places to be purchased.
    """
    clubs = generate_clubs()
    places = [12, 4, 0]
    return tuple(zip(clubs, places))


def generate_invalid_purchase_more_than_points():
    """
    Return a tuple containing tuples.
    Each of these tuples represents a club and
    a number of places to be purchased.
    However, the club does not have enough points to make the purchase.
    """
    clubs = generate_clubs()
    places = [7, 12]
    return tuple(zip(clubs[1:], places))
