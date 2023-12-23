
from django.urls import path

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .views import *


urlpatterns = [
    path('user/', users_view, {'id': None}, name='users'),
    path('user/<int:id>/', users_view, name='user'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('register/', RegisterView.as_view(), name='register'),

    path('room/', RoomView.as_view(), {'id': None}, name='rooms'),
    path('room/<int:id>/', RoomView.as_view(), name='room'),

    path('booking/', BookingView.as_view(), {'id': None}, name='bookings'),
    path('booking/<int:id>/', BookingView.as_view(), name='booking'),

    path('review/', ReviewView.as_view(), name='reviews'),
    path('review/<int:id>/', ReviewView.as_view(), name='reviews'),

    path('receipt/<int:b_id>', receipt, name='receipt')
]
