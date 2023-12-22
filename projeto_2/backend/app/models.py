import enum

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class RoomsType(enum.Enum):
    double = 'd'
    triple = 't'
    quad = 'q'
    suite = 's'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have a name')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
        )

        user.is_admin = True

        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)


class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=9, null=True, blank=True, default=None)
    address = models.CharField(max_length=100, null=True, blank=True, default=None)
    birthdate = models.DateField(null=True, blank=True, default=None)
    rooms = models.ManyToManyField('Room', through='Booking', blank=True, default=None)
    image = models.ImageField(upload_to='images/', null=True, blank=True, default=None)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


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
