from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('explore/', views.explore, name = 'explore'),
    path('LISTING/', views.listing, name = 'listing'),
    path('MESSAGE', views.messaging, name = 'messaging')

]