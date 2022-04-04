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
def new_message(new_user_sender, new_user_reciever):
    return models.Message(sender=new_user_sender,
                          reciever=new_user_reciever,
                          creation_date=CREATION_DATE,
                          message_text='test')


def save_a_message(new_message):
    new_message.sender.save()
    new_message.reciever.save()
    new_message.save()


def test_message_constructor(new_message, new_user_sender, new_user_reciever):
    assert new_message.sender == new_user_sender
    assert new_message.reciever == new_user_reciever
    assert new_message.creation_date == CREATION_DATE
    assert new_message.message_text == 'test'


def is_empty_string(string):
    for word in string:
        if word != ' ':
            return False
    return True


@pytest.mark.parametrize("empty_string", ['', ' ', '     '])
def test_is_empty_message(new_message, empty_string):
    new_message.message_text = empty_string
    assert is_empty_string(new_message.message_text)


@pytest.mark.django_db()
def test_saving_message(new_message):
    save_a_message(new_message)
    assert new_message.sender in models.User.objects.all()
    assert new_message.reciever in models.User.objects.all()
    assert new_message in models.Message.objects.all()


@pytest.mark.django_db()
def test_deletion_message(new_message):
    save_a_message(new_message)
    new_message.delete()
    assert new_message not in models.Message.objects.all()


@pytest.mark.django_db()
def test_deletion_message_after_sender(new_message):
    save_a_message(new_message)
    new_message.sender.delete()
    assert new_message not in models.Message.objects.all()


@pytest.mark.django_db()
def test_deletion_message_after_reciever(new_message):
    save_a_message(new_message)
    new_message.reciever.delete()
    assert new_message not in models.Message.objects.all()
