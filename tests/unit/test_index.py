import pytest


@pytest.mark.usefixtures("client_class")
class TestIndex:
    """Test class for '/' route"""

    def test_index_access(self):
        """Check the access to the page and if it contains the login form"""
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.status == "200 OK"
        assert '<form action="show_summary" method="post">' in response.data.decode()
