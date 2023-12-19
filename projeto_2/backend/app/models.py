from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=9, null=True, blank=True, default=None)
    address = models.CharField(max_length=100, null=True, blank=True, default=None)
    birthdate = models.DateField(null=True, blank=True, default=None)
    rooms = models.ManyToManyField('Room', through='Booking', blank=True, default=None)
    image = models.ImageField(upload_to='images/', null=True, blank=True, default=None)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(max_length=100)
    max_guests = models.IntegerField()
    bookings = models.ManyToManyField('User', through='Booking')
    image = models.ImageField(upload_to='images/', null=True, blank=True, default=None)

    TYPE_CHOICES = (
        ('d', 'Double'),
        ('t', 'Triple'),
        ('q', 'Quad'),
        ('s', 'Suite'),
    )

    type = models.CharField(max_length=1, choices=TYPE_CHOICES,
                            default='d', blank=False, null=False)

    def __str__(self):
        return self.name


class Booking(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=100, decimal_places=2)
    check_in = models.DateField()
    check_out = models.DateField()
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    extra_bed = models.BooleanField(default=False)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=500, null=False)
    date = models.DateTimeField(null=False)

    rating = models.PositiveIntegerField(validators=[MinValueValidator(
        1), MaxValueValidator(5)], default=0, blank=False, null=False)

    def __str__(self):
        return self.review
