from django.urls import include, path
from django.contrib import admin

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),
]
