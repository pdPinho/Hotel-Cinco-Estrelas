from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import User, Room, Booking, Review
from .serializers import *


### WEB SERVICES ###

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def users_view(request, id=None):
    if request.method == 'GET':
        if 'id' in request.GET:
            uid = int(request.GET['id'])
            print(uid)
            try:
                user = User.objects.get(id=uid)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(UserSerializer(user).data)
        elif 'email' in request.GET:
            email = request.GET['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(UserSerializer(user).data)
        else:
            users = User.objects.all()
            if 'num' in request.GET:
                num = int(request.GET['num'])
                users = users[:num]
            return Response(UserSerializer(users, many=True).data)

    elif request.method == 'PUT':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(ObtainAuthToken):
    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user = User.objects.get(id=user.id)  # This is needed or somehow the user loses its name
        serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': serializer.data})


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        request.auth.delete()
        return Response({'detail': 'Successfully logged out'})


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            User.objects.create_user(serializer.data.get('email'), serializer.data.get('name'), password=request.data['password'])
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomView(APIView):
    def get(self, request, id):
        if id:
            try:
                rooms = Room.objects.get(id=id)
                return Response(RoomSerializer(rooms).data)
            except Room.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            rooms = Room.objects.all()
            if 'num' in request.GET:
                num = int(request.GET['num'])
                rooms = rooms[:num]
        return Response(RoomSerializer(rooms, many=True).data)

    def put(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(RoomSerializer(serializer.data).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            room = Room.objects.get(id=id)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RoomSerializer(room, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            room = Room.objects.get(id=id)
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookingView(APIView):
    def get(self, request, id):
        if id:
            try:
                bookings = Booking.objects.get(id=id)
                return Response(BookingSerializer(bookings).data)
            except Booking.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            bookings = Booking.objects.all()
        return Response(BookingSerializer(bookings, many=True).data)

    def put(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(BookingSerializer(serializer.data).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            booking = Booking.objects.get(id=id)
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            booking = Booking.objects.get(id=id)
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewView(APIView):
    def get(self, request, id):
        if id:
            try:
                reviews = Review.objects.get(id=id)
                return Response(ReviewSerializer(reviews).data)
            except Review.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            reviews = Review.objects.all()
            if 'num' in request.GET:
                num = int(request.GET['num'])
                reviews = reviews[:num]
        return Response(ReviewSerializer(reviews, many=True).data)

    def put(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(ReviewSerializer(serializer.data).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            review = Review.objects.get(id=id)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            review = Review.objects.get(id=id)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
