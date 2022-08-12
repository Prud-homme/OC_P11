import pytest


@pytest.mark.usefixtures("client_class")
class TestIndex:
    def test_index_access(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.status == "200 OK"
        assert '<form action="show_summary" method="post">' in response.data.decode()
