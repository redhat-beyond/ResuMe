from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Resume, Comment, Rating
from django import forms
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


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # Django's default template name - posts/post_confirm_delete.html
    context_object_name = 'post'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


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
        return self.request.user == post.author


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    # Django's default template name - posts/comment_form.html
    fields = ['comment_text']

    def form_valid(self, form):
        form.instance.post = Post.objects.get(pk=self.kwargs['post_pk'])
        form.instance.author = self.request.user
        return super().form_valid(form)


class RatingCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Rating

    CHOICES = [('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)]

    # Django's default template name - posts/rating_form.html
    fields = ['design_rating', 'skill_relevance_rating',
              'grammar_rating', 'conciseness_rating']

    def test_func(self):
        """Validate that the user won't rate his own resume"""
        curr_resume = Resume.objects.get(pk=self.kwargs['post_pk'])
        return self.request.user != curr_resume.author

    def get_form(self, form_class=None):
        form = super(RatingCreateView, self).get_form(form_class)
        form.fields['design_rating'] = forms.ChoiceField(choices=self.CHOICES, widget=forms.RadioSelect)
        form.fields['skill_relevance_rating'] = forms.ChoiceField(choices=self.CHOICES, widget=forms.RadioSelect)
        form.fields['grammar_rating'] = forms.ChoiceField(choices=self.CHOICES, widget=forms.RadioSelect)
        form.fields['conciseness_rating'] = forms.ChoiceField(choices=self.CHOICES, widget=forms.RadioSelect)
        curr_resume = Resume.objects.get(pk=self.kwargs['post_pk'])
        try:
            user_rating = Rating.objects.get(author=self.request.user, resume=curr_resume)
            form.initial = user_rating.__dict__
        except Rating.DoesNotExist:
            pass
        return form

    def form_valid(self, form):
        form.instance.resume = Resume.objects.get(pk=self.kwargs['post_pk'])
        form.instance.author = self.request.user
        try:
            user_rating = Rating.objects.get(author=form.instance.author, resume=form.instance.resume)
            form.instance.pk = user_rating.pk
            user_rating.delete()
        except Rating.DoesNotExist:
            pass
        return super().form_valid(form)


def about(request):
    return render(request, 'posts/about.html', {'title': 'about'})


@login_required
def search(request):
    return render(request, 'posts/search.html', {'title': 'search'})
