from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('download_emails/', views.download_emails, name='download_emails'),
    path('select_email/', views.select_email, name='select_email'),
    path('unzip_files/', views.unzip_files, name='unzip_files'),
    path('extract_zip/', views.extract_zip, name='extract_zip'),
    path('summarize_conversations/', views.summarize_conversations, name='summarize_conversations'),
    path('summarize_file/', views.summarize_file, name='summarize_file'),
]
