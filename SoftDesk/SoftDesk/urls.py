"""
URL configuration for SoftDesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from rest_framework_nested import routers #drf-nested-routers pour gestion des urls imbriqués

from accounts.views import UserViewSet
from projects.views import ProjectViewSet, ContributorViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='user') #router de base
router.register('projects', ProjectViewSet, basename='project') #router de base
project_router = routers.NestedSimpleRouter(router, r'projects', lookup='project') # project router imbriqué
project_router.register('contributors', ContributorViewSet, basename='contributor') # project router imbriqué avec contributor

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(project_router.urls)),
]
