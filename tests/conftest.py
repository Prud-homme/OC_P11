from datetime import datetime, timedelta

import pytest

import server


@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client


@pytest.fixture
def mocker_future_competitions(mocker):
    now = datetime.now()
    datetime1 = now + timedelta(days=10)
    datetime2 = now + timedelta(days=50)
    datetime3 = now + timedelta(days=365)
    datetime4 = now + timedelta(days=800)
    competitions = [
        {
            "name": "Spring Festival",
            "date": datetime1.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "25",
        },
        {
            "name": "Fall Classic",
            "date": datetime2.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "13",
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
    mocker.patch.object(server, "competitions", competitions)


@pytest.fixture
def mocker_past_competitions(mocker):
    now = datetime.now()
    datetime1 = now - timedelta(days=10)
    datetime2 = now - timedelta(days=50)
    datetime3 = now - timedelta(days=365)
    datetime4 = now - timedelta(days=800)
    competitions = [
        {
            "name": "Spring Festival",
            "date": datetime1.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "25",
        },
        {
            "name": "Fall Classic",
            "date": datetime2.strftime("%Y-%m-%d %H:%M:%S"),
            "numberOfPlaces": "13",
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
    mocker.patch.object(server, "competitions", competitions)


@pytest.fixture
def mocker_clubs(mocker):
    clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]
    mocker.patch.object(server, "clubs", clubs)
