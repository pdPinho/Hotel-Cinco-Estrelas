from django.urls import include, path

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# TODO - IT ONLY CONTAINS INFORMATION FOR USERS (and very basic at that)
# MISSING REVIEW, BOOKING, ROOM

urlpatterns = [
    path('api/', include('app.urls')),
]
