from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='booking-dashboard'),
    path('bookings/', views.bookings, name="bookings"),
    path('bookings/<int:pk>', views.booking, name="booking"),
    path('make-booking/', views.make_booking, name="make-booking"),
]
