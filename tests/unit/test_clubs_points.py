import pytest

from tests.conftest import generate_clubs


@pytest.mark.usefixtures("client_class", "mocker_clubs")
class TestClubsPoints:
    """Test class for '/clubs_points' route"""

    @pytest.mark.parametrize("club", generate_clubs())
    def test_board_contains_clubs_and_their_points(self, club: str):
        """
        Check the access to the page and
        if the table contains all the clubs and their points
        """
        response = self.client.get(f"/clubs_points")
        assert response.status_code == 200
        assert response.status == "200 OK"

        club_name = club["name"]
        club_points = club["points"]
        assert club_name in response.data.decode()
        assert club_points in response.data.decode()
