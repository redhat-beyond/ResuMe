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
def persist_user(new_user):
    new_user.save()
    return new_user


@pytest.fixture
def new_resume(new_user):
    return Resume(author=new_user, description=DESCRIPTION)


@pytest.fixture
def persist_resume(new_resume):
    new_resume.author.save()
    new_resume.save()
    return new_resume


# -----------------------------------------------Resume tests------------------------------------------------------

@pytest.mark.django_db()
class TestResume:
    # Check that the Resume values are the same as the Resume inputs.
    def test_new_resume_input_same_as_output(self, new_resume):
        assert new_resume.author.username == USERNAME
        assert new_resume.description == DESCRIPTION

    # Check if the Resume can be referred as a post.
    def test_inheritance_of_resume_from_post(self, persist_resume):
        post = Post.objects.all().first()
        assert Post.objects.filter(resume=persist_resume).exists()
        assert hasattr(post, 'resume')
        assert not hasattr(post, 'poll')

    # Check if the Resume is saved in the database.
    def test_persist_resume(self, persist_resume):
        assert persist_resume in Resume.objects.all()

    # Check if the deletion of a Resume deletes only the Resume from database.
    def test_author_persistence_after_resume_deletion(self, persist_resume):
        user = persist_resume.author
        assert persist_resume in Resume.objects.all()
        assert user in User.objects.all()
        persist_resume.delete()
        assert persist_resume not in Resume.objects.all()
        assert user in User.objects.all()

    # Check if the deletions of the Resume's author deletes both the author and resume.
    def test_resume_deletion_after_author_deletion(self, persist_resume):
        user = persist_resume.author
        assert persist_resume in Resume.objects.all()
        assert user in User.objects.all()
        user.delete()
        assert persist_resume not in Resume.objects.all()
        assert user not in User.objects.all()

    # verify that it is impossible to create a Resume with invalid parameters.
    @pytest.mark.parametrize("user, description, expected_error",
                             [(USERNAME, DESCRIPTION, TypeError),
                              (new_user, 6, TypeError),
                              (EMAIL, DESCRIPTION, TypeError)])
    def test_resume_invalid_args(self, user, description, expected_error):
        with pytest.raises(expected_error):
            Resume(user=user, description=description)
