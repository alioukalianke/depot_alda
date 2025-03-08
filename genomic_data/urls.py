from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('upload/', views.upload_data, name='upload'),
    path('data/<int:data_id>/', views.data_detail, name='data_detail'),
    path('data/<int:data_id>/share/', views.share_data, name='share_data'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('data/<int:data_id>/analyze/', views.analyze_data, name='analyze_data'),
    path('search/', views.search_data, name='search_data'),
    path('share_data/', views.share_data, name='share_data'),
    path('data/visualize/', views.visualize_data_list, name='visualize_data_list'),
    path('data/analyze/', views.analyze_data_list, name='analyze_data_list'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('user_notifications/', views.user_notifications, name='user_notifications'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('shared_file/<int:file_id>/', views.view_shared_file, name='view_shared_file'),
    
]