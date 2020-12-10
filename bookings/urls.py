from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='booking-dashboard'),
    path('bookings/', views.my_bookings, name="my-bookings"),
    path('unapproved-bookings/', views.unapproved_bookings, name="unapproved-bookings"),
    path('approved-bookings/', views.approved_bookings, name="approved-bookings"),
    path('rejected-bookings/', views.rejected_bookings, name="rejected-bookings"),
    path('bookings/<int:pk>', views.booking, name="booking"),
    path('make-booking/', views.make_booking, name="make-booking"),
]
