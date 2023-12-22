from .models import User, Room, Booking, Review
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phone', 'address', 'birthdate', 'image')
        depth = 1


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'price', 'max_guests', 'type', 'image')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Review
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        getUser = UserSerializer(instance.user).data
        representation['user'] = getUser
        return representation
