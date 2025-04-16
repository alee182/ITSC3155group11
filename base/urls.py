from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('messages/', views.message_view, name='message'),
    path('messages/<str:username>/', views.message_view, name='message'),
    path('community/', views.community_view, name='community'),
    path('community/create/', views.create_post, name='create-post'),
    path('explore/', views.explore_view, name='explore'),
    path('community/<int:post_id>/', views.community_detail, name='community-detail'),
    path('community/delete/<int:pk>/', views.delete_post, name='delete-post'),
    path('LISTING/', views.listing, name = 'listing'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    




]