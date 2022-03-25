from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def validate_email_addr(test_email):
    try:
        validate_email(test_email)
    except ValidationError:
        raise ValidationError('Email is not valid')


class userProfile(AbstractUser):
    profile_pic = models.ImageField(default='profile-icon.png', upload_to='profiles/')
    email = models.CharField(max_length=30, primary_key=True, null=False, unique=True, validators=[validate_email_addr])
