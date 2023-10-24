from django.contrib import admin
from app.models import User, Room, Booking, Review

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Review)