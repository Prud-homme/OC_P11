from datetime import datetime, timedelta

import pytest

import server


@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client


def generate_future_competitions():
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
            "numberOfPlaces": "14",
        },
        {
            "name": "Spring Classic",
            "date": datetime3.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "7",
        },
        {
            "name": "Summer Festival",
            "date": datetime4.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "18",
        },
    ]
    return competitions


@pytest.fixture
def mocker_future_competitions(mocker):
    mocker.patch.object(server, "competitions", generate_future_competitions())


def generate_past_competitions():
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
            "numberOfPlaces": "14",
        },
        {
            "name": "Spring Classic",
            "date": datetime3.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "7",
        },
        {
            "name": "Summer Festival",
            "date": datetime4.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "18",
        },
    ]
    return competitions


@pytest.fixture
def mocker_past_competitions(mocker):
    mocker.patch.object(server, "competitions", generate_past_competitions())


def generate_clubs():
    clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "16"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "8"},
    ]
    return clubs


@pytest.fixture
def mocker_clubs(mocker):
    mocker.patch.object(server, "clubs", generate_clubs())
