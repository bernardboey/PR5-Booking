from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.template.loader import render_to_string


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
def my_bookings(request):
    return render(request, "bookings/bookings.html", {
        "bookings": models.Booking.objects.filter(user=request.user).order_by("booking_date", "start_time")
    })


@staff_member_required
def unapproved_bookings(request):
    bookings = models.Booking.objects.all().order_by("booking_date", "start_time")
    approval_form = forms.ApprovalForm()
    if request.method == "POST":
        approve = "approve" in request.POST
        booking_obj = models.Booking.objects.get(id=request.POST.get("booking_id"))
        approval_form = forms.ApprovalForm(request.POST, approved=approve, admin=request.user,
                                           booking=booking_obj)
        if approval_form.is_valid():
            approval_form.save()
            body_text = render_to_string('bookings/booking_reviewed/email.txt', {'booking': booking_obj})
            body_html = render_to_string('bookings/booking_reviewed/email.html', {'booking': booking_obj})
            subject = render_to_string('bookings/booking_reviewed/subject.txt', {'booking': booking_obj})
            send_mail(subject, body_text, None, [booking_obj.user.email], html_message=body_html)
            return HttpResponseRedirect(reverse("unapproved-bookings"))
    return render(request, "bookings/unapproved_bookings.html", {
        "unapproved_bookings": [_booking for _booking in bookings if not _booking.approved and not _booking.rejected],
        "approval_form": approval_form
    })


@staff_member_required
def approved_bookings(request):
    bookings = models.Booking.objects.all().order_by("booking_date", "start_time")
    approval_form = forms.ApprovalForm()
    if request.method == "POST":
        approve = "approve" in request.POST
        approval_form = forms.ApprovalForm(request.POST, approved=approve, admin=request.user,
                                           booking=models.Booking.objects.get(id=request.POST.get("booking_id")))
        if approval_form.is_valid():
            approval_form.save()
            return HttpResponseRedirect(reverse("approved-bookings"))
    return render(request, "bookings/approved_bookings.html", {
        "approved_bookings": [_booking for _booking in bookings if _booking.approved],
        "approval_form": approval_form
    })


@staff_member_required
def rejected_bookings(request):
    bookings = models.Booking.objects.all().order_by("booking_date", "start_time")
    approval_form = forms.ApprovalForm()
    if request.method == "POST":
        approve = "approve" in request.POST
        approval_form = forms.ApprovalForm(request.POST, approved=approve, admin=request.user,
                                           booking=models.Booking.objects.get(id=request.POST.get("booking_id")))
        if approval_form.is_valid():
            approval_form.save()
            return HttpResponseRedirect(reverse("rejected-bookings"))
    return render(request, "bookings/rejected_bookings.html", {
        "rejected_bookings": [_booking for _booking in bookings if _booking.rejected],
        "approval_form": approval_form
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
            return HttpResponseRedirect(reverse("my-bookings"))
    else:
        form = forms.BookingForm()
    return render(request, "bookings/make_booking.html", {
        "form": form
    })
