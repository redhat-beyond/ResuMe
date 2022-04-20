from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView
)
from .models import Post, Resume, Comment
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


class ResumeCreateView(LoginRequiredMixin, CreateView):
    model = Resume
    # Django's default template name - posts/post_form.html
    fields = ['description', 'resume_file']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(ResumeCreateView, self).get_context_data(**kwargs)
        ctx['title'] = 'resume-create'
        return ctx


class ResumeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Resume
    # Django's default template name - posts/post_form.html
    fields = ['description', 'resume_file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    # Django's default template name - posts/comment_form.html
    fields = ['comment_text']

    def form_valid(self, form):
        form.instance.post = Post.objects.get(pk=self.kwargs['post_pk'])
        form.instance.author = self.request.user
        return super().form_valid(form)


def about(request):
    return render(request, 'posts/about.html', {'title': 'about'})


@login_required
def search(request):
    return render(request, 'posts/search.html', {'title': 'search'})
