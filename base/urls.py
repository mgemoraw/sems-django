from django.urls import path, include
from . import views


app_name = 'base'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create-room/', views.createRoom, name='create-room'),
    path('room/<str:pk>/', views.room, name='room'),
    path('exams/', views.exam, name='exams'),
    path('results/', views.results, name='results'),
    path('bulk-upload/', views.bulk_upload, name='bulk-upload'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.user_register, name='register'),
]