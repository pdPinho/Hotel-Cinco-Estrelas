import json
from app.models import User, Room, Booking, Review
from django.http import HttpResponse


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.serializers import UserSerializer

### only user is "done"


### WEB SERVICES ###

@api_view(['GET'])
def get_user(request):
    id = int(request.GET['id'])
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(UserSerializer(user).data)

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    if 'num' in request.GET:
        num = int(request.GET['num'])
        users = users[:num]
    return Response(UserSerializer(users, many=True).data)

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_user(request):
    id = request.data['id']
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def del_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
