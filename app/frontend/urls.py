from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('signUp', views.signUp, name='signUp'),
    path('signIn', views.signIn, name='signIn'),
    path('signOut', views.signOut, name='signOut'),
    path('scoreboard', views.scoreboard, name='scoreboard'),
    path('home', views.home, name='home'),
    path('showProfile', views.showProfile, name='ShowProfile'),
    path('editProfile', views.editProfile, name='editProfile'),
    path('showHome', views.showHome, name='ShowHome'),
    path('update_game_result/', views.update_game_result, name='update_game_result'),
]
# urlpatterns = [
#     path('signup/', views.signup_view, name='signup'),  # Endpoint for sign-up form
#     path('signup_endpoint/', views.signup_view, name='signup'),
# ]
