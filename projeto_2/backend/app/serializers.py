from app.models import User, Room, Booking, Review
from rest_framework import serializers


### THIS IS NOT DONE! CURRENTLY EACH MODEL CONTAINS BUT THEIR BARE BONES ###

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'price', 'max_guests', 'booking')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'review', 'date')
