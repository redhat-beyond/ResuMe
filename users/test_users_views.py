import pytest
from django.contrib.auth.models import User


USERNAME = "testuser"
FIRSTNAME = "Test"
LASTNAME = "User"
PASSWORD = "testpass"
EMAIL = "testuser@gmail.com"


@pytest.fixture
def new_user():
    user = User(username=USERNAME, first_name=FIRSTNAME, last_name=LASTNAME, password=PASSWORD, email=EMAIL)
    user.set_password(PASSWORD)
    user.save()
    return user


@pytest.mark.django_db()
class TestProfileServerResponse:
    # Test that the login webpage loaded
    def test_login_entry_point(self, client):
        response = client.get('/login/')
        assert response.status_code == 200

    # After successfull login the user is redirected to the post page
    # Check login of admin
    def test_login_admin(self, client):
        response = client.post('/login/', {'username': 'admin', 'password': 'admin1234'})
        assert response.status_code == 302
        assert response.url == "/"

    # Check login of normal user
    def test_login_user(self, client, new_user):
        response = client.post('/login/', {'username': USERNAME, 'password': PASSWORD})
        assert response.status_code == 302
        assert response.url == '/'

    # Check redirect after logout
    def test_logout_user(self, client, new_user):
        client.post('/login/', {'username': USERNAME, 'password': PASSWORD})
        response = client.get('/logout/')
        assert response.status_code == 302
        assert response.url == '/'

    # check redirections form page if the user is not logged in
    @pytest.mark.parametrize('url', ['profile', 'direct', 'edit-profile'])
    def test_redirections(self, client, url):
        response = client.get(f'/{url}/')
        assert response.status_code == 302
        assert response.url == f'/login/?next=/{url}/'
