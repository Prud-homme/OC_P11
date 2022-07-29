import pytest

from tests.conftest import generate_clubs, generate_future_competitions


@pytest.mark.usefixtures("client_class", "mocker_clubs")
class TestPurchasePlaces:
    @pytest.mark.usefixtures("mocker_future_competitions")
    @pytest.mark.parametrize("competition", generate_future_competitions())
    @pytest.mark.parametrize("club", generate_clubs())
    @pytest.mark.parametrize("places", [17, 24, 30])
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
