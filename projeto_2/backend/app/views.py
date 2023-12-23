import io

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from django.db.models import Q
from django.http import HttpResponse, FileResponse

from reportlab.pdfgen import canvas

from .models import *
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
        uid = int(request.GET['id'])
        try:
            user = User.objects.get(id=uid)
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
        if serializer.is_valid():
            User.objects.create_user(serializer.data.get('email'), serializer.data.get('name'),
                                     password=request.data['password'])
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
            data_init = self.request.query_params.get('data_init', None)
            data_end = self.request.query_params.get('data_end', None)
            if data_init and data_end:
                rooms = Room.objects.none()

                conflicting_bookings = Booking.objects.filter(
                    # Could probably be simplified, but it works
                    Q(check_in__gte=data_init, check_out__lte=data_init) |
                    Q(check_in__gte=data_end, check_out__lte=data_end) |
                    Q(check_in__gte=data_init, check_in__lte=data_end) |
                    Q(check_out__gte=data_init, check_out__lte=data_end) |
                    Q(check_in__lte=data_init, check_out__gte=data_end)
                )
                conflicting_room_ids = conflicting_bookings.values_list('room_id', flat=True)
                for t in RoomsType:
                    if Room.objects.filter(type__exact=t.value).exists():
                        r = Room.objects.filter(type__exact=t.value).exclude(id__in=conflicting_room_ids)
                        if r.exists():
                            if len(r) > 1:
                                rooms |= r.first()
                            else:
                                rooms |= r
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
        temp_data = request.data.copy()
        temp_data['image'] = room.image
        serializer = RoomSerializer(room, data=temp_data)
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

    def put(self, request, id, *args, **kwargs):
        try:
            print(request.data)
            booking = Booking.objects.create(
                user_id=User.objects.get(id=request.data['user_id']['id']),
                room_id=Room.objects.get(id=request.data['room_id']['id']),
                check_in=request.data['check_in'],
                check_out=request.data['check_out'],
                breakfast=request.data['breakfast'],
                lunch=request.data['lunch'],
                extra_bed=request.data['extra_bed'],
                total_price=request.data['total_price']
            )
            return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            booking = Booking.objects.get(id=id)
        except Booking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        booking.user_id = User.objects.get(id=request.data['user_id']['id'])
        booking.room_id = Room.objects.get(id=request.data['room_id']['id'])
        booking.check_in = request.data['check_in']
        booking.check_out = request.data['check_out']
        booking.breakfast = request.data['breakfast']
        booking.lunch = request.data['lunch']
        booking.extra_bed = request.data['extra_bed']
        booking.total_price = request.data['total_price']
        serializer = BookingSerializer(booking)
        try:
            booking.save()
            return Response(serializer.data)        
        except:
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
        reviews = Review.objects.all()
        if 'num' in request.GET:
            num = int(request.GET['num'])
            reviews = reviews[:num]
        return Response(ReviewSerializer(reviews, many=True).data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            Review.objects.create(
                rating=serializer.validated_data.get("rating"),
                review=serializer.validated_data.get("review"),
                user=serializer.validated_data.get("user"),
                date=serializer.validated_data.get("date")
            )
            return Response({'message': 'Review submitted successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            review = Review.objects.get(id=id)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def receipt(request):
    b, r = None, None
    if request.method == 'GET':
        if b_id := request.GET.get('b_id', None):
            b = Booking.objects.get(id=b_id)
            r = Room.objects.get(id=b.room_id.id)
    else:
        return HttpResponse(content='No such booking', status=404)

    if b is None or r is None:
        return HttpResponse("Error", status=500)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    p.drawString(90, 790, "HOTEL CINCO ESTRELAS")
    p.drawString(90, 760, b.user_id.name)
    p.drawString(90, 745, b.user_id.address)
    p.drawString(90, 730, b.user_id.phone)
    p.drawString(170, 730, b.user_id.email)

    p.drawString(90, 700, "DETALHES DA RESERVA")
    p.drawString(90, 675, "De " + b.check_in.__str__() + " até " + b.check_out.__str__())
    p.drawString(90, 660, r.name)
    p.drawString(90, 645, "Preço total: " + b.total_price.__str__())
    p.drawString(90, 630, "Máximo de ocupantes (mais um em caso de cama extra): " + r.max_guests.__str__())
    p.drawString(90, 615, "Pequeno Almoço: " + b.breakfast.__str__())
    p.drawString(90, 600, "Almoço: " + b.lunch.__str__())
    p.drawString(90, 585, "Cama Extra: " + b.extra_bed.__str__())

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"Reservation_{b.user_id.name}_{b.id}.pdf")
