from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator


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
        return f"Resume {self.post_id} by {self.author}"

    def get_average_rating(self):
        ratings = self.rating_set.all()
        rating_sum = 0
        for rating in ratings:
            rating_sum += rating.get_rating_average()
        return rating_sum / len(self.rating_set.all())

    def get_design_rating(self):
        ratings = self.rating_set.all()
        rating_sum = 0
        for rating in ratings:
            rating_sum += rating.design_rating
        return rating_sum / len(self.rating_set.all())

    def get_skill_relevance_rating(self):
        ratings = self.rating_set.all()
        rating_sum = 0
        for rating in ratings:
            rating_sum += rating.skill_relevance_rating
        return rating_sum / len(self.rating_set.all())

    def get_grammar_rating(self):
        ratings = self.rating_set.all()
        rating_sum = 0
        for rating in ratings:
            rating_sum += rating.grammar_rating
        return rating_sum / len(self.rating_set.all())

    def get_conciseness_rating(self):
        ratings = self.rating_set.all()
        rating_sum = 0
        for rating in ratings:
            rating_sum += rating.conciseness_rating
        return rating_sum / len(self.rating_set.all())


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

    def get_rating_average(self):
        return (self.design_rating + self.skill_relevance_rating + self.grammar_rating + self.conciseness_rating) / 4
