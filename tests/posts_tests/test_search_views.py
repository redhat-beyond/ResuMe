import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
class TestViews:

    search_url = '/search/?searched='

    def test_searching_usernames_posts_view(self, client, persist_user, persist_post):
        '''test searching for an exist post by username,
           also testing for template and status code response'''
        response = client.get(f'{self.search_url}{persist_user.username}')
        assert response.status_code == 200
        assertTemplateUsed(response, 'posts/search.html')
        assert persist_post in response.context['posts']

    def test_serching_professions_posts_view(self, client, persist_user, persist_post):
        '''test searching for an exist post by user's profession
           also testing for template and status code response'''
        response = client.get(f'{self.search_url}{persist_user.profile.profession}')
        assert response.status_code == 200
        assertTemplateUsed(response, 'posts/search.html')
        assert persist_post in response.context['posts']

    def test_searching_descriptions_posts_view(self, client, persist_post):
        '''test searching for an exist post by post's description,
           also testing for template and status code response'''
        response = client.get(f'{self.search_url}{persist_post.description}')
        assert response.status_code == 200
        assertTemplateUsed(response, 'posts/search.html')
        assert persist_post in response.context['posts']

    def test_searching_for_a_non_existing_user_posts_in_view(self, client, persist_user, persist_post):
        '''test searching for a non exist post by username,
           also testing for template and status code response'''
        persist_user.delete()
        response = client.get(f'{self.search_url}{persist_user.username}')
        assert response.status_code == 200
        assertTemplateUsed(response, 'posts/search.html')
        assert persist_post not in response.context['posts']

    def test_searcing_a_non_existing_post_view(self, client, persist_user, persist_post):
        '''test searching for a non exist post,
           also testing for template and status code response'''
        persist_post.delete()
        response = client.get(f'{self.search_url}{persist_post.description}')
        assert response.status_code == 200
        assertTemplateUsed(response, 'posts/search.html')
        assert persist_post not in response.context['posts']
