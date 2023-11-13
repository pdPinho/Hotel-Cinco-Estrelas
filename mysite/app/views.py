from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User as user_auth
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

import datetime


#############################
#     Basic renders area
############################# 
def index(request):
    return render(request, 'index.html')


def contact(request):
    params = {
        'email': 'hotelcinco@estrelas.com',
        'contact': '+351 919293949'
    }
    return render(request, 'contact.html', params)


def about(request):
    return render(request, 'about.html')


def reviews(request):
    reviews_list = Review.objects.all().order_by('-date')
    paginator = Paginator(reviews_list, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    params = {
        'title': 'Reviews',
        'reviews': reviews_list,
        'form': review_insert_form(),
        "page_obj": page_obj
    }

    if request.method == 'POST':
        form = review_insert_form(request.POST)

        if form.is_valid():
            user = request.user
            u = User.objects.get(id=user.pk)
            review = form.cleaned_data['review']
            rating = form.cleaned_data['rating']

            Review(user=u,
                   review=review,
                   date=datetime.datetime.now(),
                   rating=rating).save()
        else:
            params['error'] = 'Invalid review. No rating selected.'
            return render(request, 'reviews.html', params)

    return render(request, 'reviews.html', params)


def error_404(request):
    return render(request, 'error_404.html')


@login_required()
def rooms(request, *args, **kwargs):
    params = {
        'title': 'Rooms',
    }

    if request.method == 'POST':
        form = BookingSearchForm(request.POST)

        if form.is_valid():
            prev_date = form.cleaned_data['data_inicial']
            next_date = form.cleaned_data['data_final']

            params['prev_date'] = prev_date
            params['next_date'] = next_date

            conflicting_bookings = Booking.objects.filter(
                # Could probably be simplified, but it works
                Q(check_in__gte=prev_date, check_out__lte=prev_date) |
                Q(check_in__gte=next_date, check_out__lte=next_date) |
                Q(check_in__gte=prev_date, check_in__lte=next_date) |
                Q(check_out__gte=prev_date, check_out__lte=next_date) |
                Q(check_in__lte=prev_date, check_out__gte=next_date)
            )
            conflicting_room_ids = conflicting_bookings.values_list('room_id', flat=True)

            if Room.objects.filter(type__exact='d').exists():
                double_rooms = Room.objects.filter(type='d')
                available_rooms = double_rooms.exclude(id__in=conflicting_room_ids)

                if len(available_rooms) > 0:
                    params['double_room'] = True
                    params['d_room'] = available_rooms[0]
                else:
                    params['double_room'] = False

            if Room.objects.filter(type__exact='t').exists():
                triple_rooms = Room.objects.filter(type='t')
                available_rooms = triple_rooms.exclude(id__in=conflicting_room_ids)

                if len(available_rooms) > 0:
                    params['triple_room'] = True
                    params['t_room'] = available_rooms[0]
                else:
                    params['triple_room'] = False

            if Room.objects.filter(type__exact='q').exists():
                quad_rooms = Room.objects.filter(type='q')
                available_rooms = quad_rooms.exclude(id__in=conflicting_room_ids)

                if len(available_rooms) > 0:
                    params['quad_room'] = True
                    params['q_room'] = available_rooms[0]
                else:
                    params['quad_room'] = False

            if Room.objects.filter(type__exact='s').exists():
                suite_rooms = Room.objects.filter(type='s')
                available_rooms = suite_rooms.exclude(id__in=conflicting_room_ids)

                if len(available_rooms) > 0:
                    params['suite_room'] = True
                    params['s_room'] = available_rooms[0]
                else:
                    params['suite_room'] = False
        else:
            params['error'] = 'Invalid date.'

    print(params)

    return render(request, 'rooms.html', params)


@login_required()
def reservar(request):
    params = {}

    if request.method == 'GET':
        if r_id := request.GET.get('id', None):
            room = Room.objects.get(id=r_id)

            params['id'] = r_id
            params['room'] = room
            match room.type:
                case 'd':
                    params['img'] = '/static/images/double.jpg'
                case 't':
                    params['img'] = '/static/images/triple.jpg'
                case 'q':
                    params['img'] = '/static/images/quadruple.jpg'
                case 's':
                    params['img'] = '/static/images/suite.jpg'

        if next_date := request.GET.get('n', None):
            params['next_date'] = next_date

        if prev_date := request.GET.get('p', None):
            params['prev_date'] = prev_date

        if not (params['id'] or params['prev_date'] or params['next_date']):
            params['error'] = 'Missing params'
    elif request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            user = request.user
            u = User.objects.get(id=user.pk)
            room = Room.objects.get(id=form.cleaned_data['room_id'])
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            breakfast = form.cleaned_data['breakfast']
            lunch = form.cleaned_data['lunch']
            extra_bed = form.cleaned_data['extra_bed']

            n_days = (check_out - check_in).days
            total_price = room.price * n_days

            if breakfast:
                total_price += 10 * n_days

            if lunch:
                total_price += 20 * n_days

            if extra_bed:
                total_price += 15 * n_days

            b = Booking(room_id=room,
                        user_id=u,
                        check_in=check_in,
                        check_out=check_out,
                        breakfast=breakfast,
                        lunch=lunch,
                        total_price=total_price,
                        extra_bed=extra_bed)
            b.save()

            return redirect('/confirmation?b_id=' + str(b.id))
    else:
        return HttpResponse(content='No such method. I can not make coffee as I am a teapot', status=418)

    return render(request, 'reservar.html', params)


@login_required()
def receipt(request):
    b, r = None, None
    if request.method == 'GET':
        if b_id := request.GET.get('b_id', None):
            b = Booking.objects.get(id=b_id)
            r = Room.objects.get(id=b.room_id.id)

            if request.user.id != b.user_id.id:
                return HttpResponse('Not Autorized', status=403)
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


def booking(request):
    if request.method == 'Post':
        return
    else:
        return render(request, 'booking.html')


def confirmation(request):
    if request.method == "GET":
        if b_id := request.GET.get('b_id', None):
            b = Booking.objects.get(id=b_id)
            r = Room.objects.get(id=b.room_id.id)

            if request.user.id != b.user_id.id:
                return HttpResponse('Not Autorized', status=403)

            params = {
                'booking': b,
                'room': r,
            }

            match r.type:
                case 'd':
                    params['img'] = '/static/images/double.jpg'
                case 't':
                    params['img'] = '/static/images/triple.jpg'
                case 'q':
                    params['img'] = '/static/images/quadruple.jpg'
                case 's':
                    params['img'] = '/static/images/suite.jpg'

            return render(request, 'confirmation.html', params)
        else:
            return HttpResponse(content='No such booking', status=404)
    else:
        return HttpResponse(content='How did you get here', status=418)


############################# 
#      Account area
############################# 
def register(request):
    if request.method == 'POST':
        form = user_insert_form(request.POST)

        if form.is_valid():
            # inserting user in database
            User(name=form.cleaned_data['name'],
                 email=form.cleaned_data['email'],
                 password=form.cleaned_data['password'],
                 phone=form.cleaned_data['phone'],
                 address=form.cleaned_data['address'],
                 birthdate=form.cleaned_data['birthdate']).save()

            # creating authentication user for given registration
            user_auth.objects.create_user(username=form.cleaned_data['name'],
                                          email=form.cleaned_data['email'],
                                          password=form.cleaned_data['password'])

            return render(request, 'register.html', {'form': form, 'insert': True})
    else:
        form = user_insert_form()
    return render(request, 'register.html', {'form': form, 'insert': False})


############################# 
#      Profile area
############################# 

@login_required()
def profile(request):
    user = User.objects.get(id=request.user.id)
    params = {
        'name': user.name,
        'email': user.email,
        'password': user.password,
        'phone': user.phone,
        'address': user.address,
        'birthdate': user.birthdate,
    }
    return render(request, 'profile.html', params)


@login_required()
# Display current user info and update it
def profile_edit(request):
    form = user_edit_form()
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = user_edit_form(request.POST)

        if form.is_valid():
            # updating user information
            user.name = form.cleaned_data['name']
            user.email = form.cleaned_data['email']
            user.password = form.cleaned_data['password']
            user.phone = form.cleaned_data['phone']
            user.address = form.cleaned_data['address']
            user.birthdate = form.cleaned_data['birthdate']
            user.save()

            # updating user authentication info
            u = user_auth.objects.get(pk=int(user.id))
            u.username = user.name
            u.email = user.email
            u.set_password(user.password)
            u.save()

            params = {
                'name': user.name,
                'email': user.email,
                'password': user.password,
                'phone': user.phone,
                'address': user.address,
                'birthdate': user.birthdate,
            }

            return render(request, 'profile.html', {'alert': "Profile updated successfully", 'params': params})
    else:
        # getting information to be displayed (placeholder)
        form = user_edit_form(
            initial={
                'name': user.name,
                'email': user.email,
                'password': user.password,
                'phone': user.phone,
                'address': user.address,
                'birthdate': user.birthdate,
                'form': form
            }
        )

    return render(request, 'user_edit.html', {'form': form, 'user': user.name})


############################# 
#       Admin area
##############################
### USER RELATED
# Get all users and display them

def superuser_check(user):
    return user.is_superuser


@login_required()
@user_passes_test(superuser_check)
def view_users(request):
    params = {
        'title': 'Users',
        'users': User.objects.all(),
    }

    return render(request, 'view_users.html', params)


@login_required()
@user_passes_test(superuser_check)
# Get information about specific user
def user_info(request, id):
    user = User.objects.get(id=id)
    # delete user
    if request.method == 'POST':
        u = user_auth.objects.get(pk=int(id))
        user.delete()
        u.delete()
        messages.success(request, 'User deleted successfully')
        return render(request, 'user_info.html')

    # show user information
    else:
        params = {
            'name': user.name,
            'email': user.email,
            'password': user.password,
            'phone': user.phone,
            'address': user.address,
            'birthdate': user.birthdate,
        }

        return render(request, 'user_info.html', params)


@login_required()
@user_passes_test(superuser_check)
# Display current user info and update it
def user_edit(request, id):
    form = user_edit_form()
    user = User.objects.get(id=id)

    if request.method == 'POST':
        form = user_edit_form(request.POST)

        if form.is_valid():
            # updating user information
            user.name = form.cleaned_data['name']
            user.email = form.cleaned_data['email']
            user.password = form.cleaned_data['password']
            user.phone = form.cleaned_data['phone']
            user.address = form.cleaned_data['address']
            user.birthdate = form.cleaned_data['birthdate']
            user.save()

            # updating user authentication info
            u = user_auth.objects.get(pk=int(id))
            u.username = user.name
            u.email = user.email
            u.set_password(user.password)
            u.save()

            messages.success(request, 'User updated successfully')
    else:
        # getting information to be displayed (placeholder)
        form = user_edit_form(initial={'name': user.name,
                                       'email': user.email,
                                       'password': user.password,
                                       'phone': user.phone,
                                       'address': user.address,
                                       'birthdate': user.birthdate,
                                       'form': form})

    return render(request, 'user_edit.html', {'form': form, 'user': user.name})


### BOOKING RELATED
# bookings
@login_required()
@user_passes_test(superuser_check)
def view_bookings(request):
    params = {
        'title': 'Bookings',
        'bookings': Booking.objects.all(),
    }

    return render(request, 'view_bookings.html', params)

@login_required()
@user_passes_test(superuser_check)
# Get information about specific user
def booking_info(request, id):
    booking = Booking.objects.get(id=id)
    # delete user
    if request.method == 'POST':
        u = user_auth.objects.get(pk=int(id))
        booking.delete()
        u.delete()
        messages.success(request, 'Booking deleted successfully')
        return render(request, 'booking_info.html')

    # show user information
    else:
        params = {
            'room_id': booking.room_id,
            'user_id': booking.user_id,
            'total_price': booking.total_price,
            'check_in': booking.check_in,
            'check_out': booking.check_out,
            'breakfast': booking.breakfast,
            'lunch': booking.lunch,
            'extra_bed': booking.extra_bed,
        }

        return render(request, 'booking_info.html', params)
    

@login_required()
@user_passes_test(superuser_check)
# Display current user info and update it
def booking_edit(request, id):
    form = booking_edit_form()
    booking = Booking.objects.get(id=id)

    if request.method == 'POST':
        form = booking_edit_form(request.POST)

        if form.is_valid():
            # updating booking information
            #booking.room_id = form.cleaned_data['room_id']
            #booking.user_id = form.cleaned_data['user_id']
            booking.total_price = form.cleaned_data['total_price']
            booking.check_in = form.cleaned_data['check_in']
            booking.check_out = form.cleaned_data['check_out']
            booking.breakfast = form.cleaned_data['breakfast']
            booking.lunch = form.cleaned_data['lunch']
            booking.extra_bed = form.cleaned_data['extra_bed']
            booking.save()

            messages.success(request, 'Booking updated successfully')
    else:
        # getting information to be displayed (placeholder)
        form = booking_edit_form(initial={'room_id': booking.room_id,
                                       'user_id': booking.user_id,
                                       'total_price': booking.total_price,
                                       'check_in': booking.check_in,
                                       'check_out': booking.check_out,
                                       'breakfast': booking.breakfast,
                                       'lunch': booking.lunch,
                                       'extra_bed': booking.extra_bed,
                                       'form': form})

    return render(request, 'booking_edit.html', {'form': form, 'booking': booking.id})



### ROOMS RELATED
# rooms
@login_required()
@user_passes_test(superuser_check)
def view_rooms(request):
    params = {
        'title': 'Rooms',
        'rooms': Room.objects.all(),
    }

    return render(request, 'view_rooms.html', params)


@login_required()
@user_passes_test(superuser_check)
# Get information about specific user
def room_info(request, id):
    room = Room.objects.get(id=id)
    # delete user
    if request.method == 'POST':
        u = user_auth.objects.get(pk=int(id))
        room.delete()
        u.delete()
        messages.success(request, 'Room deleted successfully')
        return render(request, 'room_info.html')

    # show user information
    else:
        params = {
            'name': room.name,
            'price': room.price,
            'max_guests': room.max_guests,
            'bookings': room.bookings,
            'type': room.type,
        }

        return render(request, 'room_info.html', params)
    

@login_required()
@user_passes_test(superuser_check)
# Display current room info and update it
def room_edit(request, id):
    form = room_edit_form()
    room = Room.objects.get(id=id)

    if request.method == 'POST':
        form = room_edit_form(request.POST)

        if form.is_valid():
            # updating room information
            room.name = form.cleaned_data['name']
            room.price = form.cleaned_data['price']
            room.max_guests = form.cleaned_data['max_guests']
            #room.bookings = form.cleaned_data['bookings']
            room.type = form.cleaned_data['type']
            room.save()

            messages.success(request, 'Room updated successfully')
    else:
        # getting information to be displayed (placeholder)
        form = room_edit_form(initial={'name': room.name,
                                       'price': room.price,
                                       'max_guests': room.max_guests,
                                       'type': room.type,
                                       'form': form})

    return render(request, 'room_edit.html', {'form': form, 'room': room.name})



### REVIEWS RELATED
# reviews
@login_required()
@user_passes_test(superuser_check)
def view_reviews(request):
    params = {
        'title': 'Reviews',
        'reviews': Review.objects.all(),
    }

    return render(request, 'view_reviews.html', params)


# Get information about specific review by user
@login_required()
@user_passes_test(superuser_check)
def review_info(request, id):
    review = Review.objects.get(id=id)
    # delete review
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully')
        return render(request, 'review_info.html')

    # show review information
    else:
        params = {
            'name': review.user.name,
            'date': review.date,
            'review': review.review,
        }

        return render(request, 'review_info.html', params)
