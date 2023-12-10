from django.urls import path

from app import views

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.serializers import UserSerializer

#### TODO - IT ONLY CONTAINS INFORMATION FOR USERS (and very basic at that)
# MISSING REVIEW, BOOKING, ROOM

urlpatterns = [
    path('api/user', views.get_user),
    path('api/users', views.get_users),
    path('api/usercre', views.create_user),
    path('api/userupd', views.update_user),
    path('api/userdel/<int:id>', views.del_user),
]
