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


# -----------------------------------Poll model inherited from Post-----------------------------------


class Poll(Post):

    def __str__(self):
        return f"Poll {self.post_id} by {self.author}"

    def get_amount_of_votes(self):
        votes_amount = 0
        for choice in self.choice_set.all():
            votes_amount += choice.get_amount_of_votes()
        return votes_amount


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


# ------------------------Choice model that stores one choice option of a Poll------------------------


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return f"'{self.choice_text}' of {self.poll}"

    def get_amount_of_votes(self):
        return len(self.vote_set.all())

    # get percentage of voters who voted to this choice
    def get_percentage(self):
        total_votes_amount = self.poll.get_amount_of_votes()
        if total_votes_amount <= 0:
            return 0
        else:
            return (self.get_amount_of_votes() / total_votes_amount) * 100


# ------------------------Vote model that stores a vote of a user on a Poll------------------------


class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    voted_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.voter}'s vote to {self.voted_choice}"
