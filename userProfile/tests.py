import pytest
from . import models
from django.core.exceptions import ValidationError

USERNAME = "testuser"
FIRSTNAME = "Test"
LASTNAME = "User"
PASSWORD = "testpass"
EMAIL = "testuser@gmail.com"


@pytest.fixture
def new_user():
    return models.userProfile(username=USERNAME,
                              first_name=FIRSTNAME,
                              last_name=LASTNAME,
                              password=PASSWORD,
                              email=EMAIL)


def test_new_user(new_user):
    assert new_user.username == USERNAME
    assert new_user.first_name == FIRSTNAME
    assert new_user.last_name == LASTNAME
    assert new_user.password == PASSWORD
    assert new_user.email == EMAIL
    assert new_user.profile_pic == 'profile-icon.png'


@pytest.mark.django_db()
def test_persist_user(new_user):
    new_user.save()
    assert new_user in models.userProfile.objects.all()


@pytest.mark.django_db()
def test_delete_user(new_user):
    new_user.delete()
    assert new_user not in models.userProfile.objects.all()


@pytest.mark.django_db
def test_validate_email_addr():
    try:
        user = models.userProfile(email="hj",
                                  username=USERNAME,
                                  first_name=FIRSTNAME,
                                  last_name=LASTNAME,
                                  password=PASSWORD)
        user.full_clean()
    except ValidationError:
        assert True  # The user was not created valid email successfully
    else:
        assert False  # The user was created successfully
