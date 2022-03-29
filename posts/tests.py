import pytest
from .models import Poll, PollFile, Choice
from django.contrib.auth.models import User

USERNAME = "testuser"
FIRSTNAME = "Test"
LASTNAME = "User"
PASSWORD = "testpass"
EMAIL = "testuser@gmail.com"
DESCRIPTION = "this is a test poll"
FILE1 = "Alon_Shakaroffs_resume.pdf"
FILE2 = "Olive.png"
CHOICETEXT1 = "First option"
CHOICETEXT2 = "Second option"


@pytest.fixture
def new_user():
    return User(username=USERNAME, first_name=FIRSTNAME, last_name=LASTNAME, password=PASSWORD, email=EMAIL)


@pytest.fixture
def new_poll(new_user):
    return Poll(author=new_user, description=DESCRIPTION)


@pytest.fixture
def new_pollFile(new_poll):
    return PollFile(poll=new_poll, file=FILE1)


@pytest.fixture
def new_choice(new_poll):
    return Choice(poll=new_poll, choice_text=CHOICETEXT1)


# -------------------------------------------- Poll tests --------------------------------------------


# Check that the Poll values are the same as the Poll inputs.
@pytest.mark.django_db()
def test_new_poll(new_poll):
    assert new_poll.author.username == USERNAME
    assert new_poll.author.first_name == FIRSTNAME
    assert new_poll.author.last_name == LASTNAME
    assert new_poll.author.password == PASSWORD
    assert new_poll.author.email == EMAIL
    assert new_poll.description == DESCRIPTION
    assert new_poll.amount_of_voters == 0
    assert len(new_poll.pollfile_set.all()) == 0
    assert len(new_poll.choice_set.all()) == 0
    new_poll.author.save()
    assert new_poll.author.profile.profile_pic == 'profile-icon.png'


# Check if the Poll is saved in the database and accessible via its author.
@pytest.mark.django_db()
def test_persist_poll(new_poll):
    assert new_poll not in Poll.objects.all()
    new_poll.author.save()
    new_poll.save()
    assert new_poll in Poll.objects.all()
    assert new_poll in User.objects.filter(username=USERNAME).first().poll_set.all()


# Check if Poll deletion delete only Poll from database.
@pytest.mark.django_db()
def test_delete_poll_aouthor(new_poll):
    user = new_poll.author
    user.save()
    new_poll.save()
    assert new_poll in Poll.objects.all()
    assert user in User.objects.all()
    new_poll.delete()
    assert new_poll not in Poll.objects.all()
    assert user in User.objects.all()


# Check if Poll's author deletion delete both the author and the poll.
@pytest.mark.django_db()
def test_delete_poll(new_poll):
    user = new_poll.author
    user.save()
    new_poll.save()
    assert new_poll in Poll.objects.all()
    assert user in User.objects.all()
    user.delete()
    assert new_poll not in Poll.objects.all()
    assert user not in User.objects.all()


# verify that it is impossible to create a Poll with invalid params.
def test_poll_unvalid_args():
    with pytest.raises(TypeError):
        Poll(user=USERNAME, description=DESCRIPTION)


# -------------------------------------------- PollFile tests --------------------------------------------


# Check that the PollFile values are the same as the PollFile inputs.
def test_new_pollfile(new_pollFile):
    assert new_pollFile.poll.author.username == USERNAME
    assert new_pollFile.poll.description == DESCRIPTION
    assert new_pollFile.poll.amount_of_voters == 0
    assert new_pollFile.file == FILE1


# Check if the PollFile is saved in the database and accessible via its Poll.
@pytest.mark.django_db()
def test_persist_pollfile(new_pollFile):
    assert new_pollFile not in PollFile.objects.all()
    new_pollFile.poll.author.save()
    new_pollFile.poll.save()
    new_pollFile.save()
    assert new_pollFile in PollFile.objects.all()
    assert new_pollFile in new_pollFile.poll.pollfile_set.all()


# Check if PollFile deletion delete only PollFile from database.
@pytest.mark.django_db()
def test_delete_pollfile(new_pollFile):
    user = new_pollFile.poll.author
    poll = new_pollFile.poll
    file = new_pollFile
    user.save()
    poll.save()
    file.save()
    assert poll in Poll.objects.all()
    assert user in User.objects.all()
    assert file in PollFile.objects.all()
    file.delete()
    assert poll in Poll.objects.all()
    assert user in User.objects.all()
    assert file not in PollFile.objects.all()


# Check if PollFile's poll deletion delete both PollFile and poll from database - but not the poll's author.
@pytest.mark.django_db()
def test_delete_pollfile_poll(new_pollFile):
    user = new_pollFile.poll.author
    poll = new_pollFile.poll
    file = new_pollFile
    user.save()
    poll.save()
    file.save()
    assert poll in Poll.objects.all()
    assert user in User.objects.all()
    assert file in PollFile.objects.all()
    poll.delete()
    assert poll not in Poll.objects.all()
    assert user in User.objects.all()
    assert file not in PollFile.objects.all()


# Check if PollFile's poll's author deletion delete also PollFile and database.
@pytest.mark.django_db()
def test_delete_pollfile_user(new_pollFile):
    user = new_pollFile.poll.author
    poll = new_pollFile.poll
    file = new_pollFile
    user.save()
    poll.save()
    file.save()
    assert poll in Poll.objects.all()
    assert user in User.objects.all()
    assert file in PollFile.objects.all()
    user.delete()
    assert poll not in Poll.objects.all()
    assert user not in User.objects.all()
    assert file not in PollFile.objects.all()


# Check if Poll can have several PollFiles simultaneously.
@pytest.mark.django_db()
def test_several_pollfiles(new_poll):
    user = new_poll.author
    poll = new_poll
    file1 = PollFile(poll=poll, file=FILE1)
    assert len(PollFile.objects.all()) == 0
    user.save()
    poll.save()
    file1.save()
    assert len(PollFile.objects.all()) == 1
    poll.pollfile_set.create(file=FILE2)
    assert len(PollFile.objects.all()) == 2
    assert len(poll.pollfile_set.all()) == 2


# verify that it is impossible to create a PollFile with invalid params.
def test_pollfile_unvalid_args():
    with pytest.raises(ValueError):
        PollFile(poll=USERNAME, file=FILE1)


# -------------------------------------------- Choice tests --------------------------------------------


# Check that the Choice values are the same as the Choice inputs.
def test_new_choice(new_choice):
    assert new_choice.poll.author.username == USERNAME
    assert new_choice.poll.description == DESCRIPTION
    assert new_choice.poll.amount_of_voters == 0
    assert new_choice.choice_text == CHOICETEXT1


# Check if the Choice is saved in the database and accessible via its Poll.
@pytest.mark.django_db()
def test_persist_choice(new_choice):
    assert new_choice not in Choice.objects.all()
    new_choice.poll.author.save()
    new_choice.poll.save()
    new_choice.save()
    assert new_choice in Choice.objects.all()
    assert new_choice in new_choice.poll.choice_set.all()


# Check if Choice deletion delete only Choice from database.
@pytest.mark.django_db()
def test_delete_choice(new_choice):
    user = new_choice.poll.author
    poll = new_choice.poll
    choice = new_choice
    user.save()
    poll.save()
    choice.save()
    assert poll in Poll.objects.all()
    assert user in User.objects.all()
    assert choice in Choice.objects.all()
    choice.delete()
    assert poll in Poll.objects.all()
    assert user in User.objects.all()
    assert choice not in Choice.objects.all()


# Check if Choice's poll deletion delete both Choice and poll from database - but not the poll's author.
@pytest.mark.django_db()
def test_delete_choice_poll(new_choice):
    user = new_choice.poll.author
    poll = new_choice.poll
    choice = new_choice
    user.save()
    poll.save()
    choice.save()
    assert poll in Poll.objects.all()
    assert user in User.objects.all()
    assert choice in Choice.objects.all()
    poll.delete()
    assert poll not in Poll.objects.all()
    assert user in User.objects.all()
    assert choice not in Choice.objects.all()


# Check if Choice's poll's author deletion delete also Choice and database.
@pytest.mark.django_db()
def test_delete_choice_user(new_choice):
    user = new_choice.poll.author
    poll = new_choice.poll
    choice = new_choice
    user.save()
    poll.save()
    choice.save()
    assert poll in Poll.objects.all()
    assert user in User.objects.all()
    assert choice in Choice.objects.all()
    user.delete()
    assert poll not in Poll.objects.all()
    assert user not in User.objects.all()
    assert choice not in Choice.objects.all()


# Check if Poll can have several Choices simultaneously.
@pytest.mark.django_db()
def test_several_choices(new_poll):
    user = new_poll.author
    poll = new_poll
    choice1 = Choice(poll=poll, choice_text=CHOICETEXT1)
    assert len(Choice.objects.all()) == 0
    user.save()
    poll.save()
    choice1.save()
    assert len(Choice.objects.all()) == 1
    poll.choice_set.create(choice_text=CHOICETEXT2)
    assert len(Choice.objects.all()) == 2
    assert len(poll.choice_set.all()) == 2


# Check if add_value and percentage functions work as expected.
def test_addvalue_and_percentage(new_poll):
    poll = new_poll
    choice1 = Choice(poll=poll, choice_text=CHOICETEXT1)
    choice2 = Choice(poll=poll, choice_text=CHOICETEXT2)
    assert choice1.votes == 0
    choice1.add_vote()
    assert choice1.votes == 1
    assert choice1.get_percentage() == 100.0
    assert choice2.get_percentage() == 0
    assert poll.amount_of_voters == 1
    choice1.add_vote()
    choice1.add_vote()
    choice2.add_vote()
    assert choice1.votes == 3
    assert choice2.votes == 1
    assert choice1.get_percentage() == 75.0
    assert choice2.get_percentage() == 25.0
    assert poll.amount_of_voters == 4


# verify that it is impossible to create a choice with invalid params.
def test_choice_unvalid_args():
    with pytest.raises(ValueError):
        Choice(poll=USERNAME, choice_text=CHOICETEXT1)
