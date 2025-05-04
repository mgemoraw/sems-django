"""
URL configuration for sems project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# define your api schema
schema_view = get_schema_view(
    openapi.Info(
        title='SEMS-API',
        default_version='v1',
        description='SEMS_API',
        terms_of_service="www.sems.adyamengineering.com/policies/terms",
        contact=openapi.Contact(email='contact@adyamengineering.com'),
        licence=openapi.License(name='BSD Licence'),
    ),
    public=True
)

# Your DRF views and router
# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)  # Example viewset

urlpatterns = [
    path('', include('base.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),
    

]
