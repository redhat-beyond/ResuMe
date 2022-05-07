from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
    MaxLengthValidator,
)
from django.urls import reverse

# --------------------------------- Post: parent of Poll And Resume----------------------------------


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


# ------------------------------------------- Resume-------------------------------------------------


class Resume(Post):
    resume_file = models.FileField(upload_to='files', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def __str__(self):
        return f"Resume {self.post_id} by {self.author}"

    def get_average_rating(self):
        ratings = self.rating_set.all()
        rating_sum = 0
        ratings_len = len(ratings)
        for rating in ratings:
            rating_sum += rating.get_rating_average()
        if ratings_len != 0:
            return rating_sum / ratings_len
        else:
            return 0

    def get_design_rating(self):
        ratings = self.rating_set.all()
        rating_sum = 0
        ratings_len = len(ratings)
        for rating in ratings:
            rating_sum += rating.design_rating
        if ratings_len != 0:
            return rating_sum / ratings_len
        else:
            return 0

    def get_skill_relevance_rating(self):
        ratings = self.rating_set.all()
        rating_sum = 0
        ratings_len = len(ratings)
        for rating in ratings:
            rating_sum += rating.skill_relevance_rating
        if ratings_len != 0:
            return rating_sum / ratings_len
        else:
            return 0

    def get_grammar_rating(self):
        ratings = self.rating_set.all()
        rating_sum = 0
        ratings_len = len(ratings)
        for rating in ratings:
            rating_sum += rating.grammar_rating
        if ratings_len != 0:
            return rating_sum / ratings_len
        else:
            return 0

    def get_conciseness_rating(self):
        ratings = self.rating_set.all()
        rating_sum = 0
        ratings_len = len(ratings)
        for rating in ratings:
            rating_sum += rating.conciseness_rating
        if ratings_len != 0:
            return rating_sum / ratings_len
        else:
            return 0


# ------------------------------------------- Rating-------------------------------------------------


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    design_rating = models.IntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])
    skill_relevance_rating = models.IntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])
    grammar_rating = models.IntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])
    conciseness_rating = models.IntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])

    def __str__(self):
        return f"Rating {self.rating_id} in {self.resume} by {self.author}"

    def get_absolute_url(self):
        return "/post/%i/" % self.resume.post_id

    def get_rating_average(self):
        return (self.design_rating + self.skill_relevance_rating + self.grammar_rating + self.conciseness_rating) / 4


# ------------------------------------------- Comment-------------------------------------------------

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=500, validators=[MaxLengthValidator(500)])

    def __str__(self):
        return f"Comment {self.pk} by {self.author} for post by {self.post.author}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})


# -----------------------------------Poll model inherited from Post-----------------------------------

class Poll(Post):

    def __str__(self):
        return f"Poll {self.post_id} by {self.author}"


# -----------------------------PollFile model that saves a file of a Poll-----------------------------

class PollFile(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    file = models.FileField(
        default=None,
        upload_to='files',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'jpeg'])]
        )

    def __str__(self):
        return f"File {self.pk} of {self.poll}"
