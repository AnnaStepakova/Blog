from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('edit/', views.UserEditView.as_view(), name='edit'),
    path('password/', views.PasswordUpdateView.as_view(), name='password_change'),
    path('pass_change_success/', views.password_success, name='pass_succ'),
    path('profile/<int:pk>/', views.ProfilePageView.as_view(), name='profile'),
    path('edit_profile/<int:pk>/', views.EditProfilePageView.as_view(), name='edit_profile'),
    # path('create_profile/', views.CreateProfilePageView.as_view(), name='create_profile'),
    path('profile/<int:pk>/follow/', views.follow, name='follow'),
    path('profile/<int:pk>/followers/', views.show_followers, name='followers'),
    path('profile/<int:pk>/feed/', views.show_feed, name='feed'),
    path('profile/<int:pk>/subs/', views.show_subs, name='subs'),
]