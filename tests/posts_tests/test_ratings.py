import pytest
from posts.models import Resume
from pytest_django.asserts import assertTemplateUsed
from conftest import RATER_USERNAME, RATER_PASSWORD, USERNAME, PASSWORD


@pytest.mark.django_db()
class TestRatingViews:
    def test_get_rate_page_for_valid_resume(self, client, persist_resume, persist_rater):
        resume = persist_resume
        client.login(username=RATER_USERNAME, password=RATER_PASSWORD)
        response = client.get(f'/post/{resume.pk}/rate/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'posts/rating_form.html')

    @pytest.mark.parametrize('invalid_resume', ['-1', '', 'resume'])
    def test_get_rate_page_for_invalid_resume_path(self, client, invalid_resume, persist_rater):
        client.login(username=RATER_USERNAME, password=RATER_PASSWORD)
        response = client.get(f'/post/{invalid_resume}/rate/')
        assert response.status_code == 404

    def test_get_rate_page_for_not_exist_resume(self, client):
        last_resume = Resume.objects.latest('post_id')
        client.login(username=RATER_USERNAME, password=RATER_PASSWORD)
        with pytest.raises(Resume.DoesNotExist):
            client.get(f'/post/{last_resume.post_id+1}/rate/')

    def test_rate_user_created_resume(self, client, persist_resume):
        # Note: USERNAME, PASSWORD are the username and passoword of the resume creator
        assert client.login(username=USERNAME, password=PASSWORD)
        response = client.get(f'/post/{persist_resume.post_id}/rate/')
        assert response.status_code == 403

    def test_rates_in_feed_page(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'posts/feed.html')
        assertTemplateUsed(response, 'posts/rating_view.html')

    def test_rates_in_post_view_page(self, client, persist_resume):
        response = client.get(f'/post/{persist_resume.post_id}/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'posts/post_detail.html')
        assertTemplateUsed(response, 'posts/rating_view.html')
