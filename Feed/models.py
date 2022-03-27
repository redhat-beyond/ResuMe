from django.db import models
from django.utils import timezone
from userProfile.models import userProfile
from django.core.validators import FileExtensionValidator


class Post(models.Model):
    postId = models.AutoField(primary_key=True)
    author = models.ForeignKey(userProfile, on_delete=models.CASCADE)
    description = models.TextField()
    datePosted = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Poll(Post):
    amountOfVoters = models.IntegerField(default=0)

    def __str__(self):
        return f"Poll {self.postId} by {self.author}"


class PollFile(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    file = models.FileField(
        default=None, upload_to='files',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'jpeg'])]
        )

    def __str__(self):
        return f"File {self.pk} of {self.poll}"


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"'{self.choice_text}' of {self.poll}"

    def addVote(self):
        self.votes += 1
        self.poll.amountOfVoters += 1

    def percentage(self):
        if self.poll.amountOfVoters <= 0:
            return 0
        else:
            return (self.votes / self.poll.amountOfVoters) * 100
