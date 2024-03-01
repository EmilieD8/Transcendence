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
    path('update_game_result_pong/', views.update_game_result_pong, name='update_game_result_pong'),
    path('update_game_result_memory/', views.update_game_result_memory, name='update_game_result_memory'),
    path('get_username/', views.get_username, name='get_username'),
]
