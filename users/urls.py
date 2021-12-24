from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import PostListView, PostListViewGuest

urlpatterns = [
    # path('register/', views.register, name="user-register"),
    path('login/', views.register_login, name="user-login"),
    path('register_complete/', views.confirmation, name="user-confirmation"),   
    path('logout/', views.logout_user, name="user-logout"),
    path('update_profile/', views.update_profile, name="user-profile"),
    path('update_password/', views.update_password, name="user-password"),
    path('update_picture/', views.update_picture, name="user-picture"),
    path('my_posts/', PostListView.as_view(), name="my-posts"),
    path('<str:username>/', PostListViewGuest.as_view(), name="user-posts"),  
]
