import pytest

import server


@pytest.mark.usefixtures("client_class", "mocker_clubs")
class TestPurchasePlaces:
    @pytest.mark.usefixtures("mocker_future_competitions")
    @pytest.mark.parametrize("competition", server.competitions)
    @pytest.mark.parametrize("club", server.clubs)
    @pytest.mark.parametrize("places", [3, 5, 9, 12])
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
    @pytest.mark.parametrize("competition", server.competitions)
    @pytest.mark.parametrize("club", server.clubs)
    @pytest.mark.parametrize("places", [3, 5, 9, 12])
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
    @pytest.mark.parametrize("competition", server.competitions)
    @pytest.mark.parametrize("club", server.clubs)
    @pytest.mark.parametrize("places", [3, 5, 9, 12])
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
