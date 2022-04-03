from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


# --------------------------------- Post: parent of Poll And Resume----------------------------------


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)


# ------------------------------------------- Resume-------------------------------------------------


class Resume(Post):
    resume_file = models.FileField(upload_to='files', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def __str__(self):
        return f"ResuMe {self.post_id} by {self.author}"
