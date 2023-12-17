from django.urls import include, path

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

urlpatterns = [
    path('api/', include('app.urls')),
]
