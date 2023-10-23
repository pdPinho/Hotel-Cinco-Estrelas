from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.IntegerField(max_length=100)
    address = models.CharField(max_length=100)
    birthdate = models.DateField()
    

class Room(models.Model):
    type = models.CharField(max_length=100)
    price = models.FloatField(max_length=100)
    max_guests = models.IntegerField(max_length=100)
        
        
class Booking(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    #check_in = models.DateField()
    check_in = models.DateField()
    check_out = models.DateField()