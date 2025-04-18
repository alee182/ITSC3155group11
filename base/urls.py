from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('explore/', views.explore, name = 'explore'),
    path('LISTING/', views.listing, name = 'listing'),
    path('MESSAGE', views.messaging, name = 'messaging'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('community/', views.community, name='community'),
    path('create-listing/', views.createListing, name='create-listing'),

]