import pytest
from .models import Post
from .models import Resume
from .models import Rating
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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


@pytest.fixture
def new_rating(new_resume, new_user):
    return Rating(
        author=new_user,
        resume=new_resume,
        design_rating=5,
        skill_relevance_rating=5,
        grammar_rating=5,
        conciseness_rating=5
    )


def new_user_with_name_and_email(user_name, email):
    return User(username=user_name, first_name=FIRSTNAME, last_name=LASTNAME, password=PASSWORD, email=email)


# -----------------------------------------------Resume tests------------------------------------------------------


# Check that the Resume values are the same as the Resume inputs.
def test_new_resume(new_resume):
    assert new_resume.author.username == USERNAME
    assert new_resume.description == DESCRIPTION
    assert len(new_resume.rating_set.all()) == 0


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


# Check if the Resume is saved in the database.
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


# Verify that it is impossible to create a Resume with invalid parameters.
def test_resume_invalid_args():
    with pytest.raises(TypeError):
        Resume(user=USERNAME, description=DESCRIPTION)


# Check if the resume average functions work properly
@pytest.mark.django_db()
def test_resume_average_functions(new_resume):
    grade = 5
    user_name = "user"
    email_suffix = "@gmail.com"
    new_resume.author.save()
    new_resume.save()

    for i in range(3):
        rating = Rating(
            author=new_user_with_name_and_email(user_name + str(i), user_name + str(i) + email_suffix),
            resume=new_resume,
            design_rating=grade,
            skill_relevance_rating=grade,
            grammar_rating=grade,
            conciseness_rating=grade
        )
        rating.author.save()
        rating.save()
        grade -= 2

    assert new_resume.get_average_rating() == 3
    assert new_resume.get_design_rating() == 3
    assert new_resume.get_skill_relevance_rating() == 3
    assert new_resume.get_grammar_rating() == 3
    assert new_resume.get_conciseness_rating() == 3


# -----------------------------------------------Rating tests------------------------------------------------------


# Check that the Rating values are the same as the Rating inputs.
def test_new_rating(new_rating):
    assert new_rating.author.username == USERNAME
    assert new_rating.resume.description == DESCRIPTION
    assert new_rating.design_rating == 5
    assert new_rating.skill_relevance_rating == 5
    assert new_rating.grammar_rating == 5
    assert new_rating.conciseness_rating == 5


# Check if the Rating is saved in the database.
@pytest.mark.django_db()
def test_persist_rating(new_rating):
    assert new_rating not in Rating.objects.all()
    new_rating.author.save()
    new_rating.resume.save()
    new_rating.save()
    assert new_rating in Rating.objects.all()


# Check if the deletion of a Rating deletes only the Rating from database.
@pytest.mark.django_db()
def test_delete_rating(new_rating):
    user = new_rating.author
    resume = new_rating.resume
    user.save()
    resume.save()
    new_rating.save()
    assert new_rating in Rating.objects.all()
    assert user in User.objects.all()
    assert resume in Resume.objects.all()
    new_rating.delete()
    assert new_rating not in Rating.objects.all()
    assert user in User.objects.all()
    assert resume in Resume.objects.all()


# Check if the deletions of the Rating's author deletes both the author and rating.
@pytest.mark.django_db()
def test_delete_rating_author(new_rating):
    user = new_rating.author
    user.save()
    new_rating.resume.save()
    new_rating.save()
    assert new_rating in Rating.objects.all()
    assert user in User.objects.all()
    user.delete()
    assert new_rating not in Rating.objects.all()
    assert user not in User.objects.all()


# Check if the deletions of the Rating's resume deletes both the resume and rating.
@pytest.mark.django_db()
def test_delete_rating_resume(new_rating):
    resume = new_rating.resume
    new_rating.author.save()
    resume.save()
    new_rating.save()
    assert new_rating in Rating.objects.all()
    assert resume in Resume.objects.all()
    resume.delete()
    assert new_rating not in Rating.objects.all()
    assert resume not in Resume.objects.all()


# Verify that it is impossible to create a Rating with invalid parameters.
@pytest.mark.django_db()
def test_rating_invalid_args(new_user, new_resume):
    with pytest.raises(ValidationError):
        new_user.save()
        new_resume.save()
        rating = Rating(
                author=new_user,
                resume=new_resume,
                design_rating=0,
                skill_relevance_rating=8,
                grammar_rating=5,
                conciseness_rating=5
            )
        rating.clean_fields()


# Check if the Rating average function works properly
@pytest.mark.django_db()
def test_rating_avg_function(new_rating):
    new_rating.author.save()
    new_rating.resume.save()
    new_rating.save()
    assert new_rating.get_rating_average() == 5
