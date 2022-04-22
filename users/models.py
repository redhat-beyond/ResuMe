from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='profile-icon.png', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True)
    profession = models.TextField(max_length=100, blank=True, validators=[MaxLengthValidator(100)])
    User._meta.get_field('email')._unique = True

    def __str__(self):
        return f"{self.user.username}'s Profile"

# this function resize profile pic in profile page
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)
