import pytest


@pytest.mark.django_db
class TestViews:

    def test_feed_view(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_about_view(self, client):
        response = client.get('/about/')
        assert response.status_code == 200
