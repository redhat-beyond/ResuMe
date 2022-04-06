import pytest
from .models import Resume
from .models import Comment
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Post and post author details
USERNAME = "testuser"
FIRSTNAME = "Test"
LASTNAME = "User"
PASSWORD = "testpass"
EMAIL = "testuser@gmail.com"
DESCRIPTION = "this is a test resume"
FILE1 = "Alon_Shakaroffs_resume.pdf"

# Comment and comment author details
COMMENT_USERNAME = "testCommentUser"
COMMENT_FIRSTNAME = "TestComment"
COMMENT_LASTNAME = "UserComment"
COMMENT_PASSWORD = "testpassComment"
COMMENT_EMAIL = "testcomment@gmail.com"
COMMENT = "Very nice ResuMe!"
A_VERY_LONG_COMMENT = """
                        test test test test test test test test
                        test test test test test test test test test test test test test test test
                        test test test test test test test test test test test test test test test test
                        test test test test test test test test test test test test test test test test
                        test test test test test test test test test test test test test test test test test test
                        test test test test test test test test test test test test test test test test test test test
                        test test test test test test test test test test test test test test test test test test test
                    """

# -----------------------------------------------fixtures----------------------------------------------------------


@pytest.fixture
def post_author():
    return User(username=USERNAME, first_name=FIRSTNAME, last_name=LASTNAME, password=PASSWORD, email=EMAIL)


@pytest.fixture
def persist_post_author(post_author):
    post_author.save()
    return post_author


@pytest.fixture
def new_resume(post_author):
    return Resume(author=post_author, description=DESCRIPTION)


@pytest.fixture
def persist_resume(new_resume):
    new_resume.author.save()
    new_resume.save()
    return new_resume


@pytest.fixture
def comment_author():
    return User(username=COMMENT_USERNAME,
                first_name=COMMENT_FIRSTNAME,
                last_name=COMMENT_LASTNAME,
                password=COMMENT_PASSWORD,
                email=COMMENT_EMAIL)


@pytest.fixture
def new_comment(comment_author, new_resume):
    return Comment(post=new_resume, author=comment_author, comment_text=COMMENT)


@pytest.fixture
def persist_comment(new_comment):
    new_comment.post.author.save()
    new_comment.post.save()
    new_comment.author.save()
    new_comment.save()
    return new_comment


@pytest.mark.django_db()
class TestComment:
    # Check if the Comment values are the same as comment input
    def test_save_comment(self, new_comment):
        assert new_comment.post.author.username == USERNAME
        assert new_comment.author.username == COMMENT_USERNAME
        assert new_comment.comment_text == COMMENT

    # Check if the comment is saved in the database
    def test_persist_comment(self, persist_comment):
        assert persist_comment in Comment.objects.all()

    # Check if the comment is deleted in the database
    def test_delete_comment(self, persist_comment):
        comment = persist_comment
        comment.delete()
        assert comment not in Comment.objects.all()

    # Check if deletion of resume delete the comment from database
    def test_comment_deletion_after_resume_deletion(self, persist_comment):
        comment = persist_comment
        comment.post.delete()
        assert comment.post not in Resume.objects.all()
        assert comment not in Comment.objects.all()

    # Check if the deletion of comment's author delete the comment
    def test_comment_deletion_after_comment_author_deletion(self, persist_comment):
        comment = persist_comment
        comment.author.delete()
        assert comment.author not in User.objects.all()
        assert comment not in Comment.objects.all()

    # Check comment length validation call
    def test_comment_with_invalid_comment_length(self, new_resume, comment_author):
        with pytest.raises(ValidationError):
            comment = Comment(post=new_resume, author=comment_author, comment_text=A_VERY_LONG_COMMENT)
            comment.clean_fields()
