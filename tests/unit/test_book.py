import pytest

import server


@pytest.mark.usefixtures("client_class", "mocker_clubs")
class TestBook:
    @pytest.mark.usefixtures("mocker_future_competitions")
    @pytest.mark.parametrize("competition", server.competitions)
    @pytest.mark.parametrize("club", server.clubs)
    def test_book_future_competition(self, competition, club):
        response = self.client.get(f"/book/{competition['name']}/{club['name']}")
        assert response.status_code == 200
        assert response.status == "200 OK"
        assert competition["name"] in response.data.decode()
        assert club["name"] in response.data.decode()

    @pytest.mark.usefixtures("mocker_past_competitions")
    @pytest.mark.parametrize("competition", server.competitions)
    @pytest.mark.parametrize("club", server.clubs)
    def test_book_past_competition(self, competition, club):
        response = self.client.get(f"/book/{competition['name']}/{club['name']}")
        assert response.status_code == 200
        assert response.status == "200 OK"
        assert (
            "You cannot book places for an ended competition!" in response.data.decode()
        )
