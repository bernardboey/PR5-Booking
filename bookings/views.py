from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from . import models
from . import forms


def home(request):
    return render(request, "home.html")


@login_required
def dashboard(request):
    return render(request, "bookings/dashboard.html", {
        "bookings": models.Booking.objects.all()
    })


@login_required
def bookings(request):
    return render(request, "bookings/bookings.html", {
        "bookings": models.Booking.objects.filter(user=request.user).order_by("-timestamp")
    })


@login_required
def booking(request, pk):
    return render(request, "bookings/booking.html", {
        "booking": models.Booking.objects.get(pk=pk)
    })


@login_required
def make_booking(request):
    if request.method == "POST":
        form = forms.BookingForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("bookings"))
    else:
        form = forms.BookingForm()
    return render(request, "bookings/make_booking.html", {
        "form": form
    })
