import pytest
from users.models import Profile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from conftest import USERNAME, PASSWORD, LASTNAME, FIRSTNAME, EMAIL, LONG_PROFESSION


@pytest.mark.django_db()
class TestUserModel():
    # Check if the user is saved in the database
    def test_persist_user(self, new_user):
        new_user.save()
        assert new_user in User.objects.all()
        assert new_user.profile in Profile.objects.all()

    # Check that the user values are the same as the user inputs.
    def test_new_user_input_validation_with_db(self, new_user):
        assert new_user.username == USERNAME
        assert new_user.first_name == FIRSTNAME
        assert new_user.last_name == LASTNAME
        assert new_user.check_password(PASSWORD)
        assert new_user.email == EMAIL
        new_user.save()  # Profile create just after save user
        assert new_user.profile.bio == ''
        assert new_user.profile.profession == ''
        assert new_user.profile.profile_pic == 'profile-icon.png'

    # Check if the user was deleted from the database
    def test_delete_user_from_db(self, new_user):
        new_user.save()
        new_user.delete()
        assert new_user not in User.objects.all()
        assert new_user.profile not in Profile.objects.all()

    # In this test we delete only the profile part, and check if the profile was deleted and not the whole user
    def test_delete_only_profile_from_db(self, new_user):
        new_user.save()
        new_user.profile.delete()
        assert new_user in User.objects.all()
        assert new_user.profile not in Profile.objects.all()

    # Check invalid email
    def test_validate_email_addr(self):
        with pytest.raises(ValidationError):
            user = User(
                        username=USERNAME,
                        first_name=FIRSTNAME,
                        last_name=LASTNAME,
                        password=PASSWORD,
                        email="check")
            user.full_clean()

    # Test for unique username
    def test_unique_username(self):
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
    def test_invalid_profession_length(self, new_user):
        with pytest.raises(ValidationError):
            new_user.save()
            new_user.profile.profession = LONG_PROFESSION
            new_user.profile.clean_fields()
