import pytest
from django import urls
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed


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


@pytest.mark.django_db()
class TestPostViews:
    def test_resume_creation_view_with_authenticated_user(self, client, persist_user):
        client.force_login(persist_user)
        resume_creation_path = urls.reverse('resume-create')
        assert client.get(resume_creation_path).status_code == 200
        client.logout()

    def test_resume_creation_view_without_authenticated_user(self, client):
        resume_creation_path = urls.reverse('resume-create')
        response = client.get(resume_creation_path)
        assert response.status_code == 302

    def test_not_author_resume_update_view(self, client, persist_resume):
        not_author_user = User(username='not_author_user', first_name='test', last_name='test',
                               password='test', email='user@email.com')
        not_author_user.save()
        client.force_login(not_author_user)
        resume_update_path = f'/post/resume/{persist_resume.pk}/update/'
        resume_update_response = client.get(resume_update_path)
        assert resume_update_response.status_code == 403

    def test_author_resume_update_view(self, client, persist_user, persist_resume):
        client.force_login(persist_user)
        resume_update_path = f'/post/resume/{persist_resume.pk}/update/'
        resume_update_response = client.get(resume_update_path)
        assert resume_update_response.status_code == 200
        assertTemplateUsed(resume_update_response, 'posts/resume_form.html')
