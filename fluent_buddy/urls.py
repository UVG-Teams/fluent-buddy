"""fluent_buddy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.contrib import admin
from rest_framework import routers
from django.conf.urls import url, include
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

from users.views import UserViewSet
from chatrooms.views import ChatroomViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'chatrooms', ChatroomViewSet)

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r'^api/token-auth/', obtain_jwt_token),
    url(r'^api/token-refresh/', refresh_jwt_token),
    url(r'^api/token-verify/', verify_jwt_token),
]
