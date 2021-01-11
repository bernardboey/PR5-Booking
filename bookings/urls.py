from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='booking-dashboard'),
    path('calendar/', views.calendar, name='calendar'),
    path('my-upcoming-bookings/', views.my_upcoming_bookings, name="my-upcoming-bookings"),
    path('my-pending-bookings/', views.my_pending_bookings, name="my-pending-bookings"),
    path('my-rejected-bookings/', views.my_rejected_bookings, name="my-rejected-bookings"),
    path('my-past-bookings/', views.my_past_bookings, name="my-past-bookings"),
    path('unapproved-bookings/', views.unapproved_bookings, name="unapproved-bookings"),
    path('approved-bookings/', views.approved_bookings, name="approved-bookings"),
    path('rejected-bookings/', views.rejected_bookings, name="rejected-bookings"),
    path('past-bookings/', views.past_bookings, name="past-bookings"),
    # path('bookings/<int:pk>', views.booking, name="booking"),
    path('make-booking/', views.make_booking, name="make-booking"),

    # API Routes
    path('bookings/', views.get_bookings, name="get-bookings"),
]
