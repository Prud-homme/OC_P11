import pytest
from math import floor

import server
from tests.conftest import (
    generate_clubs,
    generate_future_competitions,
    generate_past_competitions,
    generate_valid_purchase,
    generate_invalid_purchase_more_than_points,
)


@pytest.mark.usefixtures("client_class", "mocker_clubs")
class TestPurchasePlaces:
    @pytest.mark.usefixtures("mocker_future_competitions")
    @pytest.mark.parametrize("competition", generate_future_competitions())
    @pytest.mark.parametrize("club, places", generate_valid_purchase())
    def test_purchase_places_future_competition(self, competition, club, places):
        data = {
            "competition": competition["name"],
            "club": club["name"],
            "places": places,
        }

        response = self.client.post("/purchase_places", data=data)
        assert response.status_code == 200
        assert response.status == "200 OK"
        assert "Great-booking complete!" in response.data.decode()

    @pytest.mark.usefixtures("mocker_future_competitions")
    @pytest.mark.parametrize("competition", generate_future_competitions())
    @pytest.mark.parametrize("club, places", generate_valid_purchase())
    def test_method_not_allowed(self, competition, club, places):
        data = {
            "competition": competition["name"],
            "club": club["name"],
            "places": places,
        }
        get_response = self.client.get("/purchase_places")
        put_response = self.client.put("/purchase_places", data=data)
        patch_response = self.client.patch("/purchase_places", data=data)
        delete_response = self.client.delete("/purchase_places")

        assert get_response.status_code == 405
        assert put_response.status_code == 405
        assert patch_response.status_code == 405
        assert delete_response.status_code == 405

        assert get_response.status == "405 METHOD NOT ALLOWED"
        assert put_response.status == "405 METHOD NOT ALLOWED"
        assert patch_response.status == "405 METHOD NOT ALLOWED"
        assert delete_response.status == "405 METHOD NOT ALLOWED"

    @pytest.mark.usefixtures("mocker_past_competitions")
    @pytest.mark.parametrize("competition", generate_past_competitions())
    @pytest.mark.parametrize("club, places", generate_valid_purchase())
    def test_purchase_places_past_competition(self, competition, club, places):
        data = {
            "competition": competition["name"],
            "club": club["name"],
            "places": places,
        }
        response = self.client.post("/purchase_places", data=data)
        assert response.status_code == 200
        assert response.status == "200 OK"
        assert (
            "You cannot book places for an ended competition!" in response.data.decode()
        )

    @pytest.mark.usefixtures("mocker_future_competitions")
    @pytest.mark.parametrize("competition", generate_future_competitions())
    @pytest.mark.parametrize("club", generate_clubs())
    @pytest.mark.parametrize("places", [13, 1000])
    def test_club_shouldnt_book_more_than_12_places(self, competition, club, places):
        data = {
            "competition": competition["name"],
            "club": club["name"],
            "places": places,
        }
        response = self.client.post("/purchase_places", data=data)
        assert response.status_code == 302
        assert response.status == "302 FOUND"

        redirect_response = self.client.post(
            "/purchase_places", data=data, follow_redirects=True
        )
        assert redirect_response.status_code == 200
        assert redirect_response.status == "200 OK"
        assert (
            "Cannot booking more than 12 places per competition"
            in redirect_response.data.decode()
        )

    @pytest.mark.usefixtures("mocker_future_competitions")
    @pytest.mark.parametrize("competition", generate_future_competitions())
    @pytest.mark.parametrize("club", generate_clubs())
    @pytest.mark.parametrize("places", [-1, -500])
    def test_club_shouldnt_book_less_than_0_place(self, competition, club, places):
        data = {
            "competition": competition["name"],
            "club": club["name"],
            "places": places,
        }
        response = self.client.post("/purchase_places", data=data)
        assert response.status_code == 302
        assert response.status == "302 FOUND"

        redirect_response = self.client.post(
            "/purchase_places", data=data, follow_redirects=True
        )
        assert redirect_response.status_code == 200
        assert redirect_response.status == "200 OK"
        assert (
            "Cannot booking less than 0 place per competition"
            in redirect_response.data.decode()
        )

    @pytest.mark.usefixtures("mocker_future_competitions")
    @pytest.mark.parametrize("competition", generate_future_competitions())
    @pytest.mark.parametrize(
        "club, places", generate_invalid_purchase_more_than_points()
    )
    def test_club_shouldnt_use_more_than_their_points(self, competition, club, places):
        data = {
            "competition": competition["name"],
            "club": club["name"],
            "places": places,
        }

        response = self.client.post("/purchase_places", data=data)
        assert response.status_code == 302
        assert response.status == "302 FOUND"

        redirect_response = self.client.post(
            "/purchase_places", data=data, follow_redirects=True
        )
        max_places_can_book = floor(int(club["points"]) / server.POINTS_PER_PLACE)
        flash_message = f"You cannot book more than {max_places_can_book} places"
        assert redirect_response.status_code == 200
        assert redirect_response.status == "200 OK"
        assert flash_message in redirect_response.data.decode()

    @pytest.mark.usefixtures("mocker_future_competitions")
    @pytest.mark.parametrize("competition", generate_future_competitions())
    @pytest.mark.parametrize("club, places", generate_valid_purchase())
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
    @pytest.mark.usefixtures("mocker_clubs")
    @pytest.mark.parametrize("competition", generate_future_competitions())
    @pytest.mark.parametrize("club, places", generate_valid_purchase())
    def test_update_club_points(self, competition, club, places):
        data = {
            "competition": competition["name"],
            "club": club["name"],
            "places": places,
        }

        expected_remaining_points = (
            int(club["points"]) - places * server.POINTS_PER_PLACE
        )
        self.client.post("/purchase_places", data=data)

        remaining_points = int(
            [
                server_club["points"]
                for server_club in server.clubs
                if server_club["name"] == club["name"]
            ][0]
        )
        assert remaining_points == expected_remaining_points
