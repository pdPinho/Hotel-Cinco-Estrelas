from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import User, Room, Booking, Review
from .serializers import *

# only user is "done"


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


class RoomView(APIView):
    def get(self, request):
        if 'id' in request.GET:
            num = int(request.GET['id'])
            try:
                rooms = Room.objects.get(id=num)
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

    def patch(self, request):
        id = request.data['id']
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
    def get(self, request):
        if 'id' in request.GET:
            num = int(request.GET['id'])
            try:
                bookings = Booking.objects.get(id=num)
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

    def patch(self, request):
        id = request.data['id']
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
    def get(self, request):
        if 'id' in request.GET:
            num = int(request.GET['id'])
            try:
                reviews = Review.objects.get(id=num)
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

    def patch(self, request):
        id = request.data['id']
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

