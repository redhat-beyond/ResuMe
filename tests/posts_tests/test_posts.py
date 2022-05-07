import pytest
from posts.models import Post, Resume, Rating, Poll, PollFile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from conftest import RATER_USERNAME, new_user, new_poll


USERNAME = "testuser"
FIRSTNAME = "Test"
LASTNAME = "User"
PASSWORD = "testpass"
EMAIL = "testuser@gmail.com"
DESCRIPTION = "this is a test post"
FILE1 = "Alon_Shakaroffs_resume.pdf"
FILE2 = "Olive.png"


def new_user_with_name_and_email(user_name, email):
    user = User(username=user_name, first_name=FIRSTNAME, last_name=LASTNAME, password=PASSWORD, email=email)
    user.set_password(PASSWORD)
    user.save()
    return user


def new_rating_with_input(resume, author, grade):
    rating = Rating(
        author=author,
        resume=resume,
        design_rating=grade,
        skill_relevance_rating=grade,
        grammar_rating=grade,
        conciseness_rating=grade
    )
    rating.save()
    return rating


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

    # Check if the Resume average methods work properly.
    def test_resume_average_functions(self, persist_resume):
        current_grade = 5
        current_username = "test_rater"

        for i in range(1, 4):
            current_username += str(i)
            current_email = current_username + "@gmail.com"
            current_rater = new_user_with_name_and_email(current_username, current_email)
            new_rating_with_input(resume=persist_resume, author=current_rater, grade=current_grade)
            current_grade -= 2
        assert persist_resume.get_average_rating() == 3
        assert persist_resume.get_design_rating() == 3
        assert persist_resume.get_skill_relevance_rating() == 3
        assert persist_resume.get_grammar_rating() == 3
        assert persist_resume.get_conciseness_rating() == 3

    # verify that it is impossible to create a Resume with invalid parameters.
    @pytest.mark.parametrize("user, description, expected_error",
                             [(USERNAME, DESCRIPTION, TypeError),
                              (new_user, 6, TypeError),
                              (EMAIL, DESCRIPTION, TypeError)])
    def test_resume_invalid_args(self, user, description, expected_error):
        with pytest.raises(expected_error):
            Resume(user=user, description=description)


# -----------------------------------------------Rating tests------------------------------------------------------


@pytest.mark.django_db()
class TestRating:
    # Check that the Rating values are the same as the Rating inputs.
    def test_new_rating_input_same_as_output(self, new_rating):
        assert new_rating.author.username == RATER_USERNAME
        assert new_rating.resume.description == DESCRIPTION
        assert new_rating.design_rating == 5
        assert new_rating.skill_relevance_rating == 5
        assert new_rating.grammar_rating == 5
        assert new_rating.conciseness_rating == 5

    # Check if the Rating is saved in the database.
    def test_persist_rating(self, persist_rating):
        assert persist_rating in Rating.objects.all()

    # Check if the deletion of a Rating deletes only the Rating from database.
    def test_author_and_resume_persistence_after_rating_deletion(self, persist_rating):
        user = persist_rating.author
        resume = persist_rating.resume
        assert persist_rating in Rating.objects.all()
        assert user in User.objects.all()
        assert resume in Resume.objects.all()
        persist_rating.delete()
        assert persist_rating not in Rating.objects.all()
        assert user in User.objects.all()
        assert resume in Resume.objects.all()

    # Check if the deletions of the Rating's author deletes both the author and rating.
    def test_rating_deletion_after_author_deletion(self, persist_rating):
        user = persist_rating.author
        assert persist_rating in Rating.objects.all()
        assert user in User.objects.all()
        user.delete()
        assert persist_rating not in Rating.objects.all()
        assert user not in User.objects.all()

    # Check if the deletions of the Rating's resume deletes both the resume and rating.
    def test_rating_deletion_after_resume_deletion(self, persist_rating):
        resume = persist_rating.resume
        assert persist_rating in Rating.objects.all()
        assert resume in Resume.objects.all()
        resume.delete()
        assert persist_rating not in Rating.objects.all()
        assert resume not in Resume.objects.all()

    # Verify that it is impossible to create a Rating with invalid parameters.
    @pytest.mark.parametrize("design_rating,"
                             " skill_relevance_rating,"
                             " grammar_rating,"
                             " conciseness_rating,"
                             " expected_error",
                             [(0, 5, 4, 2, ValidationError),
                              (5, 5, 8, 2, ValidationError),
                              (5, 5, -1, 2, ValidationError)])
    def test_rating_invalid_args(
            self,
            design_rating,
            skill_relevance_rating,
            grammar_rating,
            conciseness_rating,
            expected_error,
            persist_user,
            persist_resume):
        with pytest.raises(expected_error):
            rating = Rating(
                    author=persist_user,
                    resume=persist_resume,
                    design_rating=design_rating,
                    skill_relevance_rating=skill_relevance_rating,
                    grammar_rating=grammar_rating,
                    conciseness_rating=conciseness_rating
                )
            rating.clean_fields()

    # Check if the Rating average function works properly
    def test_rating_avg_function(self, persist_rating):
        assert persist_rating.get_rating_average() == 5


# -------------------------------------------- Poll tests --------------------------------------------
@pytest.mark.django_db()
class TestPoll:
    # Check that the Poll values are the same as the Poll inputs.
    def test_new_poll_input_same_as_output(self, new_poll):
        assert new_poll.author.username == USERNAME
        assert new_poll.description == DESCRIPTION

    # Check if the Poll is saved in the database.
    def test_persist_poll(self, persist_poll):
        assert persist_poll in Poll.objects.all()

    # Check if the Poll can be referred as post.
    def test_inheritance_of_poll_from_post(self, persist_poll):
        assert Post.objects.filter(poll=persist_poll).exists()
        post = Post.objects.filter(poll=persist_poll).first()
        assert hasattr(post, 'poll')
        assert not hasattr(post, 'resume')

    # Check if Poll deletion delete only Poll from database.
    def test_delete_poll(self, persist_poll):
        assert persist_poll in Poll.objects.all()
        assert persist_poll.author in User.objects.all()
        persist_poll.delete()
        assert persist_poll not in Poll.objects.all()
        assert persist_poll.author in User.objects.all()

    # Check if Poll's author deletion delete both the author and the poll.
    def test_delete_polls_author(self, persist_poll):
        assert persist_poll in Poll.objects.all()
        assert persist_poll.author in User.objects.all()
        persist_poll.author.delete()
        assert persist_poll not in Poll.objects.all()
        assert persist_poll.author not in User.objects.all()

    # verify that it is impossible to create a Poll with invalid parameters.
    @pytest.mark.parametrize("user, description, expected_error", [
        (USERNAME, DESCRIPTION, ValueError),
        (new_user, 6, ValueError),
        (DESCRIPTION, new_user, ValueError)])
    def test_poll_invalid_args(self, user, description, expected_error):
        with pytest.raises(expected_error):
            Poll(author=user, description=description)


# -------------------------------------------- PollFile tests --------------------------------------------

@pytest.mark.django_db()
class TestPollFile:
    # Check that the PollFile values are the same as the PollFile inputs.
    def test_new_poll_file_input_same_as_output(self, new_poll_file):
        assert new_poll_file.poll.author.username == USERNAME
        assert new_poll_file.poll.description == DESCRIPTION
        assert new_poll_file.file == FILE1

    # Check if the PollFile is saved in the database and accessible via its Poll.
    def test_persist_poll_file(self, persist_poll_file):
        assert persist_poll_file in PollFile.objects.all()
        assert persist_poll_file in persist_poll_file.poll.pollfile_set.all()

    # Check if PollFile deletion delete only PollFile from database.
    def test_delete_pollfile(self, persist_poll_file):
        assert persist_poll_file.poll in Poll.objects.all()
        assert persist_poll_file.poll.author in User.objects.all()
        assert persist_poll_file in PollFile.objects.all()
        persist_poll_file.delete()
        assert persist_poll_file.poll in Poll.objects.all()
        assert persist_poll_file.poll.author in User.objects.all()
        assert persist_poll_file not in PollFile.objects.all()

    # Check if PollFile's poll deletion delete both PollFile and poll from database - but not the poll's author.
    def test_delete_pollfile_poll(self, persist_poll_file):
        persist_poll_file.poll.delete()
        assert persist_poll_file.poll not in Poll.objects.all()
        assert persist_poll_file.poll.author in User.objects.all()
        assert persist_poll_file not in PollFile.objects.all()

    # Check if PollFile's poll's author deletion delete also PollFile and database.
    def test_delete_pollfile_user(self, persist_poll_file):
        persist_poll_file.poll.author.delete()
        assert persist_poll_file.poll not in Poll.objects.all()
        assert persist_poll_file.poll.author not in User.objects.all()
        assert persist_poll_file not in PollFile.objects.all()

    # Check if Poll can have several PollFiles simultaneously.
    def test_several_pollfiles(self, persist_poll):
        file1 = PollFile(poll=persist_poll, file=FILE1)
        assert len(PollFile.objects.all()) == 0
        file1.save()
        assert len(PollFile.objects.all()) == 1
        persist_poll.pollfile_set.create(file=FILE2)
        assert len(persist_poll.pollfile_set.all()) == 2

    # verify that it is impossible to create a PollFile with invalid params (string as poll, User as poll, int as file).
    @pytest.mark.parametrize("poll, file, expected_error", [(
        USERNAME, DESCRIPTION, ValueError),
        (new_user, DESCRIPTION, ValueError),
        (new_poll, 6, ValueError)])
    def test_pollfile_invalid_args(self, poll, file, expected_error):
        with pytest.raises(expected_error):
            PollFile(poll=poll, file=file)
