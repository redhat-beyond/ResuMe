from django.shortcuts import render
from django.views.generic import ListView
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'posts/feed.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']  # order posts from newest to oldest

    def get_context_data(self, **kwargs):
        ctx = super(PostListView, self).get_context_data(**kwargs)
        ctx['title'] = 'feed'
        return ctx


def about(request):
    return render(request, 'posts/about.html', {'title': 'about'})


def search(request):
    return render(request, 'posts/search.html', {'title': 'search'})
