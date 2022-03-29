from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


# ---------------------------Abstract model Post: parent of Poll And Resume---------------------------


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


# -----------------------------------Poll model inherited from Post-----------------------------------


class Poll(Post):
    amount_of_voters = models.IntegerField(default=0)

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


# ------------------------Choice model that stores one choice option of a Poll------------------------


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"'{self.choice_text}' of {self.poll}"

    # add one vote to this choice
    def add_vote(self):
        self.votes += 1
        self.poll.amount_of_voters += 1

    # get percentage of voters who voted to this choice
    def get_percentage(self):
        if self.poll.amount_of_voters <= 0:
            return 0
        else:
            return (self.votes / self.poll.amount_of_voters) * 100
