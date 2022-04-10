from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='profile-icon.png', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True)
    profession = models.TextField(max_length=100, blank=True, validators=[MaxLengthValidator(100)])
    User._meta.get_field('email')._unique = True

    def __str__(self):
        return f"{self.user.username}'s Profile"
