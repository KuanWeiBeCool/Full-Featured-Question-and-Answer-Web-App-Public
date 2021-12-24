from django.urls import path, include
from blog.models import Post
from .views import (
    CommentUpdateView,
    PostCreateView,
    PostListView,
    PostDetailView,
    PostUpdateView, 
    PostDeleteView, 
    SearchResultsView,
    PostCategoryView,
    CategorySearchResultView,
    CommentDeleteView,
    LikeView,
    CommentLikeView
    # class-based views
)
from . import views # "." -> current directory

urlpatterns = [
    # Naming as "blog-home" because there may be more than one apps that have "home" page
    # Having the home page map to the views.home function
    path('like/<int:pk>', LikeView, name='like-post'),
    path('comment/like/<int:pk>', CommentLikeView, name='comment-like-post'),
    path('', PostListView.as_view() , name="blog-home"),
    path('search/', SearchResultsView.as_view() , name="search-results"),
    path('search/category/<str:category>', CategorySearchResultView.as_view() , name="search-results"),
    path('category/<str:category>', PostCategoryView.as_view() , name="category-results"),
    path('post/<int:pk>/', PostDetailView.as_view() , name="post-detail"),   # <int:pk> add to the url based on the primary key of the Post
    path('post/new/', PostCreateView.as_view() , name="post-create"),   
    path('post/<int:pk>/update', PostUpdateView.as_view() , name="post-update"),   
    path('post/<int:pk>/delete', PostDeleteView.as_view() , name="post-delete"),   
    path('comment/<int:pk>/update', CommentUpdateView.as_view() , name="comment-update"),   
    path('comment/<int:pk>/delete', CommentDeleteView.as_view() , name="comment-delete"),   
    # path('about/', views.about, name="blog-about"),
]
