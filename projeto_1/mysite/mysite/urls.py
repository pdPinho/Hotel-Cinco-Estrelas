from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import include, path, re_path

from app import views
from django.views.static import serve

from .settings import MEDIA_ROOT

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('reviews/', views.reviews, name='reviews'),
    path('error_404/', views.error_404, name='error_404'),
    path('rooms/', views.rooms, name='rooms'),
    path('reservar/', views.reservar, name='reservar'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('receipt/', views.receipt, name='receipt'),
    path('upload_file/', views.upload_file, name='upload_file'),

    ### account area ###
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/register/', views.register, name='register'),

    ### profile area ###
    path('profile/', views.profile, name='profile'),
    path("profile/password_reset/",
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset_form'),
    path("profile/password_reset/done",
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path("profile/password_reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path("profile/password_reset/complete",
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    ### admin area ###
    # users
    path('functionalities/admin/users', views.view_users, name='view_users'),
    path('functionalities/admin/users/<str:id>/', views.user_info, name='user_info'),
    path('functionalities/admin/users/<str:id>/edit/', views.user_edit, name='user_edit'),

    # bookings
    path('functionalities/admin/bookings', views.view_bookings, name='view_bookings'),
    path('functionalities/admin/bookings/<str:id>/', views.booking_info, name='booking_info'),
    path('functionalities/admin/bookings/<str:id>/edit/', views.booking_edit, name='booking_edit'),

    # rooms
    path('functionalities/admin/rooms', views.view_rooms, name='view_rooms'),
    path('functionalities/admin/rooms/<str:id>/', views.room_info, name='room_info'),
    path('functionalities/admin/rooms/<str:id>/edit/', views.room_edit, name='room_edit'),

    # reviews
    path('functionalities/admin/reviews', views.view_reviews, name='view_reviews'),
    path('functionalities/admin/reviews/<str:id>/', views.review_info, name='review_info'),

    # languages
    path("i18n/", include("django.conf.urls.i18n")),

    # media
    re_path(r"profile/media/(?P<path>.*)$", serve,
            {"document_root": MEDIA_ROOT}),
]