from . import models
import pytest
from django.utils import timezone
from django.contrib.auth.models import User


CREATION_DATE = timezone.now()


@pytest.fixture
def new_user_sender():
    return User(username='TestSender', first_name='Nick',
                last_name='Birch', password='1234', email='Nick@email.com')


@pytest.fixture
def new_user_reciever():
    return User(username='TestReciever', first_name='Andrew',
                last_name='Glouberman', password='abcd', email='Andrew@email.com')


@pytest.fixture
def message0(new_user_sender, new_user_reciever):
    return models.Message(sender=new_user_sender,
                          reciever=new_user_reciever,
                          creation_date=CREATION_DATE,
                          message_text='test')


def save_a_message(message0):
    message0.sender.save()
    message0.reciever.save()
    message0.save()


def test_new_message_fields(message0, new_user_sender, new_user_reciever):
    assert message0.sender == new_user_sender
    assert message0.reciever == new_user_reciever
    assert message0.creation_date == CREATION_DATE
    assert message0.message_text == 'test'


def is_empty_string(string):
    for word in string:
        if word != ' ':
            return False
    return True


@pytest.mark.parametrize("empty_string", ['', ' ', "     "])
def test_is_empty_message(message0, empty_string):
    message0.message_text = empty_string
    assert is_empty_string(message0.message_text)


@pytest.mark.django_db()
def test_saving_message(message0):
    save_a_message(message0)
    assert message0.sender in models.User.objects.all()
    assert message0.reciever in models.User.objects.all()
    assert message0 in models.Message.objects.all()


@pytest.mark.django_db()
def test_deletion_message(message0):
    save_a_message(message0)
    message0.delete()
    assert message0 not in models.Message.objects.all()


@pytest.mark.django_db()
def test_deletion_message_after_sender(message0):
    save_a_message(message0)
    message0.sender.delete()
    assert message0 not in models.Message.objects.all()


@pytest.mark.django_db()
def test_deletion_message_after_reciever(message0):
    save_a_message(message0)
    message0.reciever.delete()
    assert message0 not in models.Message.objects.all()
