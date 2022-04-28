import pytest
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed
from conftest import USERNAME, PASSWORD


def save_user(user):
    try:
        user = User.objects.get(username=USERNAME)
        return user
    except User.DoesNotExist:
        user.save()
        return user


@pytest.mark.django_db()
class TestProfileServerResponse:
    def test_login_page_loaded(self, client):
        response = client.get('/login/')
        assert response.status_code == 200
        assert 'users/login.html' in response.template_name

    def test_valid_login_user(self, client, new_user):
        new_user.save()
        assert client.login(username=USERNAME, password=PASSWORD)

    def test_invalid_login_user(self, client):
        assert not client.login(username="Not_valid", password="Not_valid")

    def test_redirection_to_main_page_after_login(self, client, new_user):
        new_user.save()
        response = client.post('/login/', {'username': USERNAME, 'password': PASSWORD})
        assert response.status_code == 302
        response = client.get(response.url)
        assert response.status_code == 200
        assert 'posts/feed.html', 'posts/post_list.html' in response.template_name

    def test_redirection_to_main_page_after_logout(self, client, new_user):
        new_user.save()
        client.login(username=USERNAME, password=PASSWORD)
        response = client.get('/logout/')
        assert response.status_code == 302
        response = client.get(response.url)
        assert response.status_code == 200
        assert 'posts/feed.html', 'posts/post_list.html' in response.template_name

    @pytest.mark.parametrize('url', ['profile', 'edit-profile'])
    def test_redirections_to_login_page_for_not_logget_in_user(self, client, url):
        response = client.get(f'/{url}/')
        assert response.status_code == 302
        assert response.url == f'/login/?next=/{url}/'
        response = client.get(response.url)
        assert 'users/login.html' in response.template_name

    @pytest.mark.parametrize('url', ['profile', 'edit-profile', 'users/admin'])
    def test_redirect_unauthorized_user(self, client, url):
        response = client.get(f'/{url}/')
        assert response.status_code == 302
        assert response.url == f'/login/?next=/{url}/'
        response = client.get(response.url)
        assert 'users/login.html' in response.template_name

    @pytest.mark.parametrize('url, template_file', [('profile', 'users/profile.html'),
                                                    ('edit-profile', 'users/edit-profile.html'),
                                                    ('users/admin', 'users/profile_details.html')
                                                    ]
                             )
    def test_authorized_user_pages_access(self, client, url, template_file, new_user):
        save_user(new_user)
        client.login(username=USERNAME, password=PASSWORD)
        response = client.get(f'/{url}/')
        assert response.status_code == 200
        assertTemplateUsed(response, template_file)

    def test_access_to_valid_user_profile(self, client, new_user):
        user = save_user(new_user)
        client.login(username='MatanPeretz', password='matan1234')
        response = client.get(f'/users/{user.username}/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/profile_details.html')

    @pytest.mark.parametrize('invalid_profile', ['Jonathan', '', '12', '1', '-1', ''])
    def test_access_to_invalid_user_profile(self, client, invalid_profile, new_user):
        save_user(new_user)
        client.login(username=USERNAME, password=PASSWORD)
        response = client.get(f'/users/{invalid_profile}/')
        assert response.status_code == 404
