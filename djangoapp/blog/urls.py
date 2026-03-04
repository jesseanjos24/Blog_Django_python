
from django.contrib import admin
from django.urls import path
from blog.views import PostListView, PostDetailView, PageDetailView, CriatedByListView, CtegoryListViews, TagListViews, SearchListView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post'),
    path('page/<slug:slug>/', PageDetailView.as_view(), name='page'),
    path('created_by/<int:autor_url>/', CriatedByListView.as_view(), name='create_by'),
    path('category/<slug:slug>/', CtegoryListViews.as_view(), name='category'),
    path('tag/<slug:slug>/', TagListViews.as_view(), name='tag'),
    path('search/', SearchListView.as_view(), name='search'),
]
