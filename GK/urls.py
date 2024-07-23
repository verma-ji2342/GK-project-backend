"""
URL configuration for GK project.

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
from rest_framework.routers import DefaultRouter
from home.views import PersonViewSet
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication


from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="GK-backend",
        default_version='v1.2',
        description="My API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="pranjal.verma@coriolis.co.in"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(JWTAuthentication,),
)



router = DefaultRouter()
router.register(r'persons', PersonViewSet)

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]