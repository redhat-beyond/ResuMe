import pytest
from .models import Post, Resume, Rating, Poll, PollFile, Choice
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

USERNAME = "testuser"
FIRSTNAME = "Test"
LASTNAME = "User"
PASSWORD = "testpass"
EMAIL = "testuser@gmail.com"
DESCRIPTION = "this is a test post"
FILE1 = "Alon_Shakaroffs_resume.pdf"
FILE2 = "Olive.png"
CHOICETEXT1 = "First option"
CHOICETEXT2 = "Second option"

# -----------------------------------------------fixtures----------------------------------------------------------


@pytest.fixture
def new_user():
    return User(username=USERNAME, first_name=FIRSTNAME, last_name=LASTNAME, password=PASSWORD, email=EMAIL)


@pytest.fixture
def new_user2():
    return User(username="user2", first_name=FIRSTNAME, last_name=LASTNAME, password=PASSWORD, email="test2@gmail.com")


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


@pytest.fixture
def persist_rating(new_rating):
    new_rating.author.save()
    new_rating.resume.save()
    new_rating.save()
    return new_rating


@pytest.fixture
def new_poll(new_user):
    return Poll(author=new_user, description=DESCRIPTION)


@pytest.fixture
def persist_poll(new_poll):
    new_poll.author.save()
    new_poll.save()
    return new_poll


@pytest.fixture
def new_poll_file(new_poll):
    return PollFile(poll=new_poll, file=FILE1)


@pytest.fixture
def persist_poll_file(new_poll_file):
    new_poll_file.poll.author.save()
    new_poll_file.poll.save()
    new_poll_file.save()
    return new_poll_file


@pytest.fixture
def new_choice(new_poll):
    return Choice(poll=new_poll, choice_text=CHOICETEXT1)


@pytest.fixture
def persist_choice(new_choice):
    new_choice.poll.author.save()
    new_choice.poll.save()
    new_choice.save()
    return new_choice


def new_user_with_name_and_email(user_name, email):
    user = User(username=user_name, first_name=FIRSTNAME, last_name=LASTNAME, password=PASSWORD, email=email)
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
        assert new_rating.author.username == USERNAME
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
        post = Post.objects.all().first()
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
    @pytest.mark.parametrize("user, description, expected_error", [(
        USERNAME,
        DESCRIPTION,
        TypeError),
        (new_user, 6, TypeError), (EMAIL, DESCRIPTION, TypeError)])
    def test_poll_invalid_args(self, user, description, expected_error):
        with pytest.raises(expected_error):
            Poll(user=user, description=description)


# -------------------------------------------- PollFile tests --------------------------------------------


@pytest.mark.django_db()
class TestPollFile:

    # Check that the PollFile values are the same as the PollFile inputs.
    def test_new_poll_file_input_same_as_output(self, new_poll_file):
        assert new_poll_file.poll.author.username == USERNAME
        assert new_poll_file.poll.description == DESCRIPTION
        assert new_poll_file.file == FILE1

    # Check if the PollFile is saved in the database and accessible via its Poll.
    @pytest.mark.django_db()
    def test_persist_poll_file(self, persist_poll_file):
        assert persist_poll_file in PollFile.objects.all()
        assert persist_poll_file in persist_poll_file.poll.pollfile_set.all()

    # Check if PollFile deletion delete only PollFile from database.
    @pytest.mark.django_db()
    def test_delete_pollfile(self, persist_poll_file):
        assert persist_poll_file.poll in Poll.objects.all()
        assert persist_poll_file.poll.author in User.objects.all()
        assert persist_poll_file in PollFile.objects.all()
        persist_poll_file.delete()
        assert persist_poll_file.poll in Poll.objects.all()
        assert persist_poll_file.poll.author in User.objects.all()
        assert persist_poll_file not in PollFile.objects.all()

    # Check if PollFile's poll deletion delete both PollFile and poll from database - but not the poll's author.
    @pytest.mark.django_db()
    def test_delete_pollfile_poll(self, persist_poll_file):
        persist_poll_file.poll.delete()
        assert persist_poll_file.poll not in Poll.objects.all()
        assert persist_poll_file.poll.author in User.objects.all()
        assert persist_poll_file not in PollFile.objects.all()

    # Check if PollFile's poll's author deletion delete also PollFile and database.
    @pytest.mark.django_db()
    def test_delete_pollfile_user(self, persist_poll_file):
        persist_poll_file.poll.author.delete()
        assert persist_poll_file.poll not in Poll.objects.all()
        assert persist_poll_file.poll.author not in User.objects.all()
        assert persist_poll_file not in PollFile.objects.all()

    # Check if Poll can have several PollFiles simultaneously.
    @pytest.mark.django_db()
    def test_several_pollfiles(self, persist_poll):
        file1 = PollFile(poll=persist_poll, file=FILE1)
        assert len(PollFile.objects.all()) == 0
        file1.save()
        assert len(PollFile.objects.all()) == 1
        persist_poll.pollfile_set.create(file=FILE2)
        assert len(persist_poll.pollfile_set.all()) == 2

    # verify that it is impossible to create a PollFile with invalid params.
    @pytest.mark.parametrize("poll, file, expected_error", [(
        USERNAME, DESCRIPTION, ValueError),
        (new_user, DESCRIPTION, ValueError),
        (new_poll, 6, ValueError)])
    def test_pollFile_invalid_args(self, poll, file, expected_error):
        with pytest.raises(expected_error):
            PollFile(poll=poll, file=file)


# -------------------------------------------- Choice tests --------------------------------------------


@pytest.mark.django_db()
class TestChoice:

    # Check that the Choice values are the same as the Choice inputs.
    def test_new_choice_input_same_as_output(self, new_choice):
        assert new_choice.poll.author.username == USERNAME
        assert new_choice.poll.description == DESCRIPTION
        assert new_choice.poll.get_amount_of_votes() == 0
        assert new_choice.choice_text == CHOICETEXT1

    # Check if the Choice is saved in the database and accessible via its Poll.
    def test_persist_choice(self, persist_choice):
        assert persist_choice in Choice.objects.all()
        assert persist_choice in persist_choice.poll.choice_set.all()

    # Check if Choice deletion delete only Choice from database.
    def test_delete_choice(self, persist_choice):
        persist_choice.delete()
        assert persist_choice.poll in Poll.objects.all()
        assert persist_choice.poll.author in User.objects.all()
        assert persist_choice not in Choice.objects.all()

    # Check if Choice's poll deletion delete both Choice and poll from database - but not the poll's author.
    def test_delete_choice_poll(self, persist_choice):
        persist_choice.poll.delete()
        assert persist_choice.poll not in Poll.objects.all()
        assert persist_choice.poll.author in User.objects.all()
        assert persist_choice not in Choice.objects.all()

    # Check if Choice's poll's author deletion delete also Choice and database.
    def test_delete_choice_user(self, persist_choice):
        persist_choice.poll.author.delete()
        assert persist_choice not in Poll.objects.all()
        assert persist_choice.poll.author not in User.objects.all()
        assert persist_choice not in Choice.objects.all()

    # Check if Poll can have several Choices simultaneously.
    def test_several_choices(self, persist_poll):
        choice1 = Choice(poll=persist_poll, choice_text=CHOICETEXT1)
        assert len(Choice.objects.all()) == 0
        choice1.save()
        assert len(Choice.objects.all()) == 1
        persist_poll.poll.choice_set.create(choice_text=CHOICETEXT2)
        assert len(persist_poll.choice_set.all()) == 2

    # verify that it is impossible to create a Choice with invalid params.
    @pytest.mark.parametrize("poll, choice_text, expected_error", [(
        USERNAME, CHOICETEXT1, ValueError),
        (new_user, DESCRIPTION, ValueError),
        (new_poll, 6, ValueError)])
    def test_pollFile_invalid_args(self, poll, choice_text, expected_error):
        with pytest.raises(expected_error):
            PollFile(poll=poll, file=choice_text)


# -------------------------------------------- votes tests --------------------------------------------


@pytest.mark.django_db()
class TestVote:

    # Check if a vote is saved in the database and accessible via its voted choice and voter.
    def test_persist_vote(self, persist_choice, persist_user):
        assert persist_user not in persist_choice.voters.all()
        persist_choice.voters.add(persist_user)
        assert persist_user in persist_choice.voters.all()
        assert persist_choice in persist_user.choice_set.all()

    # Check if vote removal works.
    def test_remove_vote(self, persist_choice, persist_user):
        persist_choice.voters.add(persist_user)
        persist_choice.voters.remove(persist_user)
        assert persist_user not in persist_choice.voters.all()

    # Check if Choice can have several Votes simultaneously.
    def test_several_votes_on_one_choice(self, persist_choice, persist_user):
        persist_choice.voters.add(persist_user)
        persist_choice.voters.create(
            username="user2",
            first_name=FIRSTNAME,
            last_name=LASTNAME,
            password=PASSWORD,
            email="test2@gmail.com")
        assert len(persist_choice.voters.all()) == 2

    # Check if Choice can have several Votes simultaneously.
    def test_several_votes_choices_of_one_user(self, persist_poll, persist_user):
        choice1 = persist_poll.choice_set.create(choice_text=CHOICETEXT1)
        choice2 = persist_poll.choice_set.create(choice_text=CHOICETEXT2)
        choice1.voters.add(persist_user)
        choice2.voters.add(persist_user)
        assert len(persist_user.choice_set.all()) == 2

    # Check if percentage function work as expected.
    def test_percentage_and_get_amount_of_voters_functions(self, persist_poll):
        user1 = User.objects.create(
            username="user1",
            first_name="uaser1",
            last_name="test",
            password="12345",
            email="user1@gmail.com")
        user2 = User.objects.create(
            username="user2",
            first_name="uaser2",
            last_name="test",
            password="12345",
            email="user2@gmail.com")
        user3 = User.objects.create(
            username="user3",
            first_name="uaser3",
            last_name="test",
            password="12345",
            email="user3@gmail.com")
        user4 = User.objects.create(
            username="user4",
            first_name="uaser4",
            last_name="test",
            password="12345",
            email="user4@gmail.com")
        choice1 = persist_poll.choice_set.create(choice_text=CHOICETEXT1)
        choice2 = persist_poll.choice_set.create(choice_text=CHOICETEXT2)
        assert choice1.get_amount_of_votes() == 0
        choice1.voters.add(user1)
        assert choice1.get_amount_of_votes() == 1
        assert choice1.get_percentage() == 100.0
        assert choice2.get_percentage() == 0
        assert persist_poll.get_amount_of_votes() == 1
        choice1.voters.add(user2)
        choice1.voters.add(user3)
        choice2.voters.add(user4)
        assert choice1.get_amount_of_votes() == 3
        assert choice2
        assert choice1.get_percentage() == 75.0
        assert choice2.get_percentage() == 25.0
        assert persist_poll.get_amount_of_votes() == 4
