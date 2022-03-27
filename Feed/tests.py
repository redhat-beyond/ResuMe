import pytest
from . import models
from userProfile.models import userProfile

USERNAME = "testuser"
FIRSTNAME = "Test"
LASTNAME = "User"
PASSWORD = "testpass"
EMAIL = "testuser@gmail.com"
DESCRIPTION = "this is a test poll"
VALIDFILE1 = "Alon_Shakaroffs_resume.pdf"
VALIDFILE2 = "asn1chapter2.pdf"
CHOICETEXT1 = "First option"
CHOICETEXT2 = "Second option"


@pytest.fixture
def new_user():
    return userProfile(username=USERNAME, first_name=FIRSTNAME, last_name=LASTNAME, password=PASSWORD, email=EMAIL)


@pytest.fixture
def new_poll(new_user):
    return models.Poll(author=new_user, description=DESCRIPTION)


@pytest.fixture
def new_pollFile(new_poll):
    return models.PollFile(poll=new_poll, file=VALIDFILE1)


@pytest.fixture
def new_choice(new_poll):
    return models.Choice(poll=new_poll, choice_text=CHOICETEXT1)


# ----------------------------------poll tests----------------------------------


def test_new_poll(new_poll):
    assert new_poll.author.username == USERNAME
    assert new_poll.author.first_name == FIRSTNAME
    assert new_poll.author.last_name == LASTNAME
    assert new_poll.author.password == PASSWORD
    assert new_poll.author.email == EMAIL
    assert new_poll.author.profile_pic == 'profile-icon.png'
    assert new_poll.description == DESCRIPTION
    assert new_poll.amountOfVoters == 0
    assert len(new_poll.pollfile_set.all()) == 0
    assert len(new_poll.choice_set.all()) == 0


@pytest.mark.django_db()
def test_persist_poll(new_poll):
    assert new_poll not in models.Poll.objects.all()
    new_poll.author.save()
    new_poll.save()
    assert new_poll in models.Poll.objects.all()
    assert new_poll == models.Poll.objects.filter(description=DESCRIPTION).first()
    assert new_poll in userProfile.objects.filter(username=USERNAME).first().poll_set.all()


@pytest.mark.django_db()
def test_delete_poll(new_poll):
    user = new_poll.author
    user.save()
    new_poll.save()
    assert new_poll in models.Poll.objects.all()
    assert user in userProfile.objects.all()
    new_poll.delete()
    assert new_poll not in models.Poll.objects.all()
    assert user in userProfile.objects.all()
    new_poll.save()
    assert new_poll in models.Poll.objects.all()
    user.delete()
    assert new_poll not in models.Poll.objects.all()
    assert user not in userProfile.objects.all()


# ----------------------------------pollFile tests----------------------------------


def test_new_pollFile(new_pollFile):
    assert new_pollFile.poll.author.username == USERNAME
    assert new_pollFile.poll.description == DESCRIPTION
    assert new_pollFile.poll.amountOfVoters == 0
    assert new_pollFile.file == VALIDFILE1


@pytest.mark.django_db()
def test_persist_pollFile(new_pollFile):
    assert new_pollFile not in models.PollFile.objects.all()
    new_pollFile.poll.author.save()
    new_pollFile.poll.save()
    new_pollFile.save()
    assert new_pollFile in models.PollFile.objects.all()
    assert new_pollFile in userProfile.objects.filter(username=USERNAME).first().poll_set.first().pollfile_set.all()
    assert new_pollFile in new_pollFile.poll.pollfile_set.all()


@pytest.mark.django_db()
def test_delete_pollFile(new_pollFile):
    user = new_pollFile.poll.author
    poll = new_pollFile.poll
    file = new_pollFile
    user.save()
    poll.save()
    file.save()
    assert poll in models.Poll.objects.all()
    assert user in userProfile.objects.all()
    assert file in models.PollFile.objects.all()
    file.delete()
    assert poll in models.Poll.objects.all()
    assert user in userProfile.objects.all()
    assert file not in models.PollFile.objects.all()
    file.save()
    poll.delete()
    assert poll not in models.Poll.objects.all()
    assert user in userProfile.objects.all()
    assert file not in models.PollFile.objects.all()


@pytest.mark.django_db()
def test_delete_user(new_pollFile):
    user = new_pollFile.poll.author
    poll = new_pollFile.poll
    file = new_pollFile
    user.save()
    poll.save()
    file.save()
    assert poll in models.Poll.objects.all()
    assert user in userProfile.objects.all()
    assert file in models.PollFile.objects.all()
    user.delete()
    assert poll not in models.Poll.objects.all()
    assert user not in userProfile.objects.all()
    assert file not in models.PollFile.objects.all()


@pytest.mark.django_db()
def test_several_pollFiles(new_poll):
    user = new_poll.author
    poll = new_poll
    file1 = models.PollFile(poll=poll, file=VALIDFILE1)
    assert len(models.PollFile.objects.all()) == 0
    user.save()
    poll.save()
    file1.save()
    assert len(models.PollFile.objects.all()) == 1
    poll.pollfile_set.create(file=VALIDFILE2)
    assert len(models.PollFile.objects.all()) == 2
    assert len(poll.pollfile_set.all()) == 2
    assert file1 == poll.pollfile_set.filter(id=file1.pk).first()


# ----------------------------------Choice tests----------------------------------


def test_new_choice(new_choice):
    assert new_choice.poll.author.username == USERNAME
    assert new_choice.poll.description == DESCRIPTION
    assert new_choice.poll.amountOfVoters == 0
    assert new_choice.choice_text == CHOICETEXT1


@pytest.mark.django_db()
def test_persist_choice(new_choice):
    assert new_choice not in models.Choice.objects.all()
    new_choice.poll.author.save()
    new_choice.poll.save()
    new_choice.save()
    assert new_choice in models.Choice.objects.all()
    assert new_choice in userProfile.objects.filter(username=USERNAME).first().poll_set.first().choice_set.all()
    assert new_choice in new_choice.poll.choice_set.all()


@pytest.mark.django_db()
def test_delete_choice(new_choice):
    user = new_choice.poll.author
    poll = new_choice.poll
    choice = new_choice
    user.save()
    poll.save()
    choice.save()
    assert poll in models.Poll.objects.all()
    assert user in userProfile.objects.all()
    assert choice in models.Choice.objects.all()
    choice.delete()
    assert poll in models.Poll.objects.all()
    assert user in userProfile.objects.all()
    assert choice not in models.Choice.objects.all()
    choice.save()
    poll.delete()
    assert poll not in models.Poll.objects.all()
    assert user in userProfile.objects.all()
    assert choice not in models.Choice.objects.all()


@pytest.mark.django_db()
def test_delete_user_choice(new_choice):
    user = new_choice.poll.author
    poll = new_choice.poll
    choice = new_choice
    user.save()
    poll.save()
    choice.save()
    assert poll in models.Poll.objects.all()
    assert user in userProfile.objects.all()
    assert choice in models.Choice.objects.all()
    user.delete()
    assert poll not in models.Poll.objects.all()
    assert user not in userProfile.objects.all()
    assert choice not in models.Choice.objects.all()


@pytest.mark.django_db()
def test_several_choices(new_poll):
    user = new_poll.author
    poll = new_poll
    choice1 = models.Choice(poll=poll, choice_text=CHOICETEXT1)
    assert len(models.Choice.objects.all()) == 0
    user.save()
    poll.save()
    choice1.save()
    assert len(models.Choice.objects.all()) == 1
    poll.choice_set.create(choice_text=CHOICETEXT2)
    assert len(models.Choice.objects.all()) == 2
    assert len(poll.choice_set.all()) == 2
    assert choice1 == poll.choice_set.filter(id=choice1.pk).first()


def test_functions(new_poll):
    poll = new_poll
    choice1 = models.Choice(poll=poll, choice_text=CHOICETEXT1)
    choice2 = models.Choice(poll=poll, choice_text=CHOICETEXT2)
    assert choice1.votes == 0
    choice1.addVote()
    assert choice1.votes == 1
    assert choice1.percentage() == 100.0
    assert choice2.percentage() == 0
    assert poll.amountOfVoters == 1
    choice1.addVote()
    choice1.addVote()
    choice2.addVote()
    assert choice1.votes == 3
    assert choice2.votes == 1
    assert choice1.percentage() == 75.0
    assert choice2.percentage() == 25.0
    assert poll.amountOfVoters == 4
