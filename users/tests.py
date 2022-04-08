import pytest
from .models import Profile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError


USERNAME = "testuser"
FIRSTNAME = "Test"
LASTNAME = "User"
PASSWORD = "testpass"
EMAIL = "testuser@gmail.com"
LONG_PROFESSION = " test test test test test test test test" \
                 " test test test test test test test test test" \
                 " test test test test test test test test test" \
                 " test test test test "


@pytest.fixture
def new_user():
    return User(username=USERNAME, first_name=FIRSTNAME, last_name=LASTNAME, password=PASSWORD, email=EMAIL)


# Check if the user is saved in the database
@pytest.mark.django_db()
def test_persist_user(new_user):
    new_user.save()
    assert new_user in User.objects.all()
    assert new_user.profile in Profile.objects.all()


# Check that the user values are the same as the user inputs.
@pytest.mark.django_db()
def test_new_user_validation_with_db(new_user):
    assert new_user.username == USERNAME
    assert new_user.first_name == FIRSTNAME
    assert new_user.last_name == LASTNAME
    assert new_user.password == PASSWORD
    assert new_user.email == EMAIL
    new_user.save()  # Profile create just after save user
    assert new_user.profile.bio == ''
    assert new_user.profile.profession == ''
    assert new_user.profile.profile_pic == 'profile-icon.png'


# Check if the user was deleted from the database
@pytest.mark.django_db()
def test_delete_user(new_user):
    new_user.save()
    new_user.delete()
    assert new_user not in User.objects.all()
    assert new_user.profile not in Profile.objects.all()


# In this test we delete only the profile part, and check if the profile was deleted and not the whole user
@pytest.mark.django_db()
def test_delete_profile(new_user):
    new_user.save()
    new_user.profile.delete()
    assert new_user in User.objects.all()
    assert new_user.profile not in Profile.objects.all()


# Check invalid email
@pytest.mark.django_db
def test_validate_email_addr():
    with pytest.raises(ValidationError):
        user = User(
                    username=USERNAME,
                    first_name=FIRSTNAME,
                    last_name=LASTNAME,
                    password=PASSWORD,
                    email="check")
        user.full_clean()


# Test for unique username
@pytest.mark.django_db
def test_unique_username():
    with pytest.raises(IntegrityError):
        user1 = User(
                    username="test",
                    first_name=FIRSTNAME,
                    last_name=LASTNAME,
                    password=PASSWORD,
                    email=EMAIL)
        user2 = User(
                    username="test",
                    first_name=FIRSTNAME,
                    last_name=LASTNAME,
                    password=PASSWORD,
                    email="test@gmail.com")
        user1.save()
        user2.save()


# Test for invalid profession length
@pytest.mark.django_db
def test_invalid_profession_length(new_user):
    with pytest.raises(ValidationError):
        new_user.save()
        new_user.profile.profession = LONG_PROFESSION
        new_user.profile.clean_fields()
