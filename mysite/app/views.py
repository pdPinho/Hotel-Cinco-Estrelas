from django.shortcuts import redirect, render
from .models import *
from app.forms import *
from django.contrib import messages
from django.contrib.auth.models import User as user_auth

############################# 
#      Basic renders
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

def error_404(request):
    return render(request, 'error_404.html')


############################# 
#      Account related
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
            user_auth.objects.create_user(username = form.cleaned_data['name'],
                                          email = form.cleaned_data['email'],
                                          password = form.cleaned_data['password'])
            
            return render(request, 'register.html', {'form': form, 'insert': True})
    else:
        form = user_insert_form()
    return render(request, 'register.html', {'form': form, 'insert': False})


############################# 
#       Admin related
##############################
### USER RELATED
# Get all users and display them
def view_users(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('/error_404')
    
    params = {
        'title': 'Users',
        'users': User.objects.all(),
    }
        
    return render(request, 'view_users.html', params)

# Get information about specific user
def user_info(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('/error_404')
    
    user = User.objects.get(id=id)
    params = {
        'name': user.name,
        'email': user.email,
        'password': user.password,
        'phone': user.phone,
        'address': user.address,
        'birthdate': user.birthdate,
    }
    
    return render(request, 'user_info.html', params)

# Display current user info and update it
def user_edit(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('/error_404')
    
    form = user_edit_form()
    user = User.objects.get(id=id)
    
    if request.method == 'POST':
        form = user_edit_form(request.POST)
        
        if form.is_valid():
            username = user.name
            
            # updating user information
            user.name=form.cleaned_data['name']
            user.email=form.cleaned_data['email']
            user.password=form.cleaned_data['password']
            user.phone=form.cleaned_data['phone']
            user.address=form.cleaned_data['address']
            user.birthdate=form.cleaned_data['birthdate']
            user.save()

            # updating user authentication info
            u = user_auth.objects.get(username=username)
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

# Delete user
def user_delete(request, id):
    pass

### BOOKING RELATED
# bookings
def view_bookings(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('/error_404')
    
    params = {
        'title': 'Bookings',
        'bookings': Booking.objects.all(),
    }
        
    return render(request, 'view_bookings.html', params)

# rooms
def view_rooms(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('/error_404')
    
    params = {
        'title': 'Rooms',
        'rooms': Room.objects.all(),
    }
        
    return render(request, 'view_rooms.html', params)

# reviews
def view_reviews(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('/error_404')
    
    params = {
        'title': 'Reviews',
        'reviews': Review.objects.all(),
    }
        
    return render(request, 'view_reviews.html', params)