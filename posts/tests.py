import pytest
from .models import Post
from .models import Resume
from django.contrib.auth.models import User

USERNAME = "testuser"
FIRSTNAME = "Test"
LASTNAME = "User"
PASSWORD = "testpass"
EMAIL = "testuser@gmail.com"
DESCRIPTION = "this is a test resume"
FILE1 = "Alon_Shakaroffs_resume.pdf"


# -----------------------------------------------fixtures----------------------------------------------------------

@pytest.fixture
def new_user():
    return User(username=USERNAME, first_name=FIRSTNAME, last_name=LASTNAME, password=PASSWORD, email=EMAIL)


@pytest.fixture
def new_resume(new_user):
    return Resume(author=new_user, description=DESCRIPTION)


# -----------------------------------------------Resume tests------------------------------------------------------


# Check that the Poll values are the same as the Poll inputs.
def test_new_resume(new_resume):
    assert new_resume.author.username == USERNAME
    assert new_resume.description == DESCRIPTION
    # assert len(new_resume.rating_set.all()) == 0  #add after adding rating


# Check if the Resume can be referred as a post.
@pytest.mark.django_db()
def test_resume_as_post(new_resume):
    assert len(Post.objects.all()) == 0
    new_resume.author.save()
    new_resume.save()
    assert len(Post.objects.all()) == 1
    post = Post.objects.all().first()
    assert hasattr(post, 'resume') is True
    assert hasattr(post, 'poll') is False
    resume = post.resume
    assert new_resume == resume


# Check if the Resume is saved in the database and is accessible via its author.
@pytest.mark.django_db()
def test_persist_resume(new_resume):
    assert new_resume not in Resume.objects.all()
    new_resume.author.save()
    new_resume.save()
    assert new_resume in Resume.objects.all()


# Check if the deletion of a Resume deletes only the Resume from database.
@pytest.mark.django_db()
def test_delete_resume(new_resume):
    user = new_resume.author
    user.save()
    new_resume.save()
    assert new_resume in Resume.objects.all()
    assert user in User.objects.all()
    new_resume.delete()
    assert new_resume not in Resume.objects.all()
    assert user in User.objects.all()


# Check if the deletions of the Resume's author deletes both the author and resume.
@pytest.mark.django_db()
def test_delete_resume_author(new_resume):
    user = new_resume.author
    user.save()
    new_resume.save()
    assert new_resume in Resume.objects.all()
    assert user in User.objects.all()
    user.delete()
    assert new_resume not in Resume.objects.all()
    assert user not in User.objects.all()


# verify that it is impossible to create a Resume with invalid parameters.
def test_poll_invalid_args():
    with pytest.raises(TypeError):
        Resume(user=USERNAME, description=DESCRIPTION)
