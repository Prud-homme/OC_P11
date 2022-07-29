import pytest

import server
from tests.conftest import generate_future_competitions, generate_clubs


@pytest.mark.usefixtures("client_class", "mocker_clubs")
class TestPurchasePlaces:
    @pytest.mark.usefixtures("mocker_future_competitions")
    @pytest.mark.parametrize("competition", generate_future_competitions())
    @pytest.mark.parametrize("club", generate_clubs())
    @pytest.mark.parametrize("places", [0, -2, 10, 14])
    def test_update_competition_number_of_places(self, competition, club, places):
        data = {
            "competition": competition["name"],
            "club": club["name"],
            "places": places,
        }
        expected_remaining_places = int(competition["numberOfPlaces"]) - places
        self.client.post("/purchase_places", data=data)
        remaining_places = int(
            [
                server_competition["numberOfPlaces"]
                for server_competition in server.competitions
                if server_competition["name"] == competition["name"]
            ][0]
        )
        assert remaining_places == expected_remaining_places

    @pytest.mark.usefixtures("mocker_future_competitions")
    @pytest.mark.parametrize("competition", generate_future_competitions())
    @pytest.mark.parametrize("club", generate_clubs())
    @pytest.mark.parametrize("places", [0, -2, 10, 14])
    def test_update_club_points(self, competition, club, places):
        data = {
            "competition": competition["name"],
            "club": club["name"],
            "places": places,
        }
        expected_remaining_points = int(club["points"]) - places
        self.client.post("/purchase_places", data=data)

        remaining_points = int(
            [
                server_club["points"]
                for server_club in server.clubs
                if server_club["name"] == club["name"]
            ][0]
        )
        assert remaining_points == expected_remaining_points
