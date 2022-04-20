import pytest
from pytest_django.asserts import assertTemplateUsed
from django import urls
from django.contrib.auth.models import User

from conftest import EMPTY_COMMENT, LONG_COMMENT, VALID_COMMENT


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

    def test_comment_creation_view_with_authenticated_user(self, client, persist_user, persist_resume):
        client.force_login(persist_user)
        comment_creation_path = f'/post/{persist_resume.pk}/comment/'
        comment_creation_response = client.get(comment_creation_path)
        assert comment_creation_response.status_code == 200
        assertTemplateUsed(comment_creation_response, 'posts/comment_form.html')
        client.logout()

    def test_comment_creation_view_without_authenticated_user(self, client, persist_resume):
        comment_creation_path = f'/post/{persist_resume.pk}/comment/'
        comment_creation_response = client.get(comment_creation_path, follow=False)
        assert comment_creation_response.status_code == 302
        comment_creation_response = client.get(comment_creation_path, follow=True)
        assert comment_creation_response.status_code == 200
        assertTemplateUsed(comment_creation_response, 'users/login.html')

    def test_comment_creation_view_with_valid_comment(self, client, persist_user, persist_resume):
        client.force_login(persist_user)
        comment_creation_path = f'/post/{persist_resume.pk}/comment/'
        create_comment_response = client.post(comment_creation_path, {'comment_text': VALID_COMMENT})
        assert create_comment_response.status_code == 302
        assert create_comment_response['Location'] == f'/post/{persist_resume.pk}/'
        client.logout()

    @pytest.mark.parametrize("invalid_comment", [(LONG_COMMENT), (EMPTY_COMMENT)])
    def test_comment_creation_view_with_invalid_comment(self, client, persist_user, persist_resume, invalid_comment):
        client.force_login(persist_user)
        comment_creation_path = f'/post/{persist_resume.pk}/comment/'
        create_comment_response = client.post(comment_creation_path, {'comment_text': invalid_comment})
        assert create_comment_response.status_code == 200
        assertTemplateUsed(create_comment_response, 'posts/comment_form.html')
        client.logout()
