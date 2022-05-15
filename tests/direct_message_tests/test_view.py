from pytest_django.asserts import assertTemplateUsed
import pytest


@pytest.mark.django_db
class TestMessagesViews:
    def test_direct_message_main_view_without_authentication(self, client, persist_user):
        client.force_login(persist_user)
        client.logout()
        response = client.get('/direct/')
        assert response.status_code == 302
        respone_redirect_path = '/login/?next=/direct/'
        response_redirect = client.get(respone_redirect_path)
        assert response_redirect.status_code == 200
        assertTemplateUsed(response_redirect, 'users/login.html')
        client.logout()

    def test_direct_message_main_view_with_authentication(self, client, persist_user):
        client.force_login(persist_user)
        response = client.get('/direct/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'direct_message/main_messages.html')
        client.logout()

    def test_direct_message_view_without_authentication(self, client, persist_user):
        client.logout()
        response = client.get(f'/direct/{persist_user.id}/')
        assert response.status_code == 302
        respone_redirect_path = '/login/?next=/direct/{persist_user.id}/'
        response_redirect = client.get(respone_redirect_path)
        assert response_redirect.status_code == 200
        assertTemplateUsed(response_redirect, 'users/login.html')

    def test_direct_message_view_with_authentication(self, client, persist_user, persist_second_user):
        client.force_login(persist_user)
        response = client.get(f'/direct/{persist_second_user.id}/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'direct_message/direct_message.html')
        client.logout()

    def test_direct_message_create_view_without_authentication(self, client, persist_user):
        client.logout()
        response = client.get(f'/direct/{persist_user.id}/new/')
        assert response.status_code == 302
        respone_redirect_path = '/login/?next=/direct/{persist_user.id}/new/'
        response_redirect = client.get(respone_redirect_path)
        assert response_redirect.status_code == 200
        assertTemplateUsed(response_redirect, 'users/login.html')

    def test_direct_message_create_view_with_authentication(self, client, persist_user, persist_second_user):
        client.force_login(persist_user)
        response = client.get(f'/direct/{persist_second_user.id}/new/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'direct_message/message_form.html')
        client.logout()

    def test_current_user_not_in_direct_message_main(self, client, persist_user):
        client.force_login(persist_user)
        response = client.get('/direct/')
        assert response.context['Users'].filter(pk=persist_user.id).count() == 0
        client.logout()

    def test_sending_new_message_to_receiver_view(self, client, persist_user, persist_second_user):
        client.force_login(persist_user)
        response = client.get(f'/direct/{persist_second_user.id}/new/')
        response = client.post(f'/direct/{persist_second_user.id}/new/', {'message_text': 'test'}, follow=True)
        assert response.status_code == 200
        assertTemplateUsed(response, 'direct_message/direct_message.html')
        client.logout()
