from django.urls import include, path, re_path
from django.contrib import admin
from .settings import MEDIA_ROOT
from django.views.static import serve

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),

    re_path(r"images/(?P<path>.*)$", serve,
            {"document_root": MEDIA_ROOT}),
]
