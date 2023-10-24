from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=9)
    address = models.CharField(max_length=100)
    birthdate = models.DateField()
    
    def __str__(self):
        return self.name

class Room(models.Model):
    type = models.CharField(max_length=100)
    price = models.FloatField(max_length=100)
    max_guests = models.IntegerField()
        
    def __str__(self):
        return self.type
        
class Booking(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=500)
    date = models.DateField()
    
    def __str__(self):
        return self.review