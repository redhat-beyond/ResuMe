from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    ResumeCreateView,
    ResumeUpdateView,
    CommentCreateView,
)
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name='posts-feed'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/resume', ResumeCreateView.as_view(), name='resume-create'),
    path('post/resume/<int:pk>/update/', ResumeUpdateView.as_view(), name='resume-update'),
    path('about/', views.about, name='posts-about'),
    path('search/', views.search, name='posts-search'),
    path('post/<int:post_pk>/comment/', CommentCreateView.as_view(), name='comment-create'),
]
