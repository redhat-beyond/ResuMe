from direct_message.models import Message
from django.contrib.auth.models import User
import pytest
from conftest import CREATION_DATE


def save_a_message(new_message):
    new_message.sender.save()
    new_message.receiver.save()
    new_message.save()


def test_new_message_validation_with_db(new_message, new_user_sender, new_user_receiver):
    assert new_message.sender == new_user_sender
    assert new_message.receiver == new_user_receiver
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
def test_saving_message_in_db(new_message):
    save_a_message(new_message)
    assert new_message.sender in User.objects.all()
    assert new_message.receiver in User.objects.all()
    assert new_message in Message.objects.all()


@pytest.mark.django_db()
def test_deletion_message_from_db(new_message):
    save_a_message(new_message)
    new_message.delete()
    assert new_message not in Message.objects.all()


@pytest.mark.django_db()
def test_deletion_message_after_sender_deletion(new_message):
    save_a_message(new_message)
    new_message.sender.delete()
    assert new_message not in Message.objects.all()


@pytest.mark.django_db()
def test_deletion_message_after_receiver_deletion(new_message):
    save_a_message(new_message)
    new_message.receiver.delete()
    assert new_message not in Message.objects.all()
