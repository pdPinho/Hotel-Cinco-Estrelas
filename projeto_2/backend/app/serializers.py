from app.models import User, Room, Booking, Review
from rest_framework import serializers


### THIS IS NOT DONE! CURRENTLY EACH MODEL CONTAINS BUT THEIR BARE BONES ###

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'phone', 'address', 'birthdate', 'rooms', 'image')
        
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'price', 'max_guests', 'booking')
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'room_id', 'user_id', 'total_price', 'check_in', 'check_out', 'breakfast', 'lunch', 'extra_bed')
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'review', 'date')
