import pytest

from tests.conftest import generate_clubs


@pytest.mark.usefixtures("client_class", "mocker_clubs")
class TestShowSummary:
    """Test class for '/show_summary' route"""

    @pytest.mark.parametrize("club", generate_clubs())
    def test_successful_login(self, club):
        """Check that club can log in with a valid email"""
        email = club["email"]
        response = self.client.post(f"/show_summary", data={"email": email})
        assert response.status_code == 200
        assert response.status == "200 OK"
        assert email in response.data.decode()

    @pytest.mark.parametrize(
        "email", ["azerty@example.com", "john@simplylift.c", "@simplylift.co", "john"]
    )
    def test_unknown_email(self, email):
        """
        Checks that the connection is impossible with a bad email
        and that the server does not crash
        """
        response = self.client.post(f"/show_summary", data={"email": email})
        assert response.status_code == 200
        assert response.status == "200 OK"
        assert "Sorry, that email wasn&#39;t found." in response.data.decode()
