from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from django.contrib.auth.decorators import login_required


class PostListView(ListView):
    model = Post
    template_name = 'posts/feed.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']  # order posts from newest to oldest

    def get_context_data(self, **kwargs):
        ctx = super(PostListView, self).get_context_data(**kwargs)
        ctx['title'] = 'feed'
        return ctx


class PostDetailView(DetailView):
    model = Post
    # Django's default template name - posts/post_detail.html
    context_object_name = 'post'


def about(request):
    return render(request, 'posts/about.html', {'title': 'about'})


@login_required
def search(request):
    return render(request, 'posts/search.html', {'title': 'search'})
