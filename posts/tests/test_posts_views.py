import pytest


@pytest.mark.django_db
class TestViews:

    def test_feed_view(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_about_view(self, client):
        response = client.get('/about/')
        assert response.status_code == 200

    def test_resume_detail_view(self, client, persist_resume):
        resume_detail_path = f'/post/{persist_resume.pk}/'
        resume_detail_response = client.get(resume_detail_path)
        assert resume_detail_response.status_code == 200

    def test_poll_detail_view(self, client, persist_poll):
        poll_detail_path = f'/post/{persist_poll.pk}/'
        poll_detail_response = client.get(poll_detail_path)
        assert poll_detail_response.status_code == 200
