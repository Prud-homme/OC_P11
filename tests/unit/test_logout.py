import pytest


@pytest.mark.usefixtures("client_class")
class TestLogout:
    def test_logout_redirection(self):
        response = self.client.get("/logout")
        assert response.status_code == 302
        assert response.status == "302 FOUND"
        redirect_response = self.client.get("/logout", follow_redirects=True)
        assert redirect_response.status_code == 200
        assert redirect_response.status == "200 OK"
        assert "Successful logout!" in redirect_response.data.decode()
