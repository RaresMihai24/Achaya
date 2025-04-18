from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('feed/', views.feed_dragon, name='feed_dragon'),
    path('breed/', views.breed_dragon, name='breed_dragon'),
    path('dragon/<str:name>/', views.view_dragon, name='view_dragon'),
    path('action/<str:action>/', views.action_dragon, name='action_dragon'),
	path('rename/', views.rename_dragon, name='rename_dragon'),
    path('auth/', views.auth_view, name='auth'),
	path('logout/', views.logout_view, name='logout'),
	path('dragons/', views.dragon_list, name='dragon_list'),
	path('accounts/login/', views.auth_view, name='login'),
    # Define additional action endpoints as needed:
    # path('water/', views.water_dragon, name='water_dragon'),
    # path('play/', views.play_dragon, name='play_dragon'),
    # ... etc.
]