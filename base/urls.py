from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('messages/', views.message_view, name='message'),
    path('messages/<str:username>/', views.message_view, name='message'),
    path('community/', views.community_view, name='community'),
    path('community/create/', views.create_post, name='create-post'),
    path('community/<int:post_id>/', views.community_detail, name='community-detail'),
    path('community/delete/<int:pk>/', views.delete_post, name='delete-post'),

    path('auth/', views.login_register, name='login_register'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    # path('profile/', views.profile, name='profile'),
    # path('profile/edit/', views.edit_profile, name='edit_profile'),

    # path('profile/edit/picture/', views.edit_profile_pic, name='edit_profile_pic'),
    # path('profile/edit/email/', views.edit_email, name='edit_email'),
    # path('profile/edit/first-name/', views.edit_first_name, name='edit_first_name'),
    # path('profile/edit/last-name/', views.edit_last_name, name='edit_last_name'),

    path('sales/', views.sales_page, name='sales'),
    path('sales/create/', views.create_sale, name='create_sale'),
    path('sales/edit/<int:pk>/', views.edit_sale, name='edit_sale'),
    path('sales/delete/<int:pk>/', views.delete_sale, name='delete_sale'),
    
    path('explore/', views.explore, name='explore'),
    path('explore/<int:pk>/', views.explore_detail, name='explore_detail'),


]