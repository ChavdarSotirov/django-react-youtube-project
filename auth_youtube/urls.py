from django.urls import path, include

from auth_youtube.views import register_user, user_profile, sighout_user

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', register_user, name='register user'),
    path('user_profile/<int:pk>/', user_profile, name='user profile'),
    path('profile/', user_profile, name='current user profile'),
    path('signout/', sighout_user, name='signout user'),

]
