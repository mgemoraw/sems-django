from django.urls import path, include
from .views import home, login, logout

app_name = 'base'

urlpatterns = [
    path('', home, name='home'),
    path('', login, name='login'),
    path('', logout, name='logout'),
]