from django.urls import path, include
from . import views


app_name = 'base'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('create-room/', views.createRoom, name='create-room'),
    path('room/<str:pk>/', views.room, name='room'),
    path('exams/', views.exam, name='exams'),
    path('results/', views.results, name='results'),
    path('bulk-upload/', views.bulk_upload, name='bulk-upload'),
    path('profile/', views.profile, name='profile'),
]