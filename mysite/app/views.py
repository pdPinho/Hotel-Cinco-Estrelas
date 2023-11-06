from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User as user_auth
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q

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
                Q(check_in__lte=prev_date) | Q(check_in__lte=next_date) | Q(check_out__gte=prev_date) | Q(
                    check_out__gte=next_date)
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

def booking(request):
    
    if request.method == 'Post':
        return
    else:
        return render(request, 'booking.html')
    
        


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
