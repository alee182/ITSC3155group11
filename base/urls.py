from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('messages/', views.message_view, name='message'),
    path('messages/<str:username>/', views.message_view, name='message'),
    path('community/', views.community_view, name='community'),
    path('community/create/', views.create_post, name='create-post'),

]