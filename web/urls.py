from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('',views.ytdownload,name='ytdownload'),
    path('api/video_download/', views.VideoDownloadAPIView.as_view(), name='video_download_api'),
]
