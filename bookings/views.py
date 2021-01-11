from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.template.loader import render_to_string

from datetime import datetime
import dateutil.parser

from . import models
from . import forms


def home(request):
    return render(request, "home.html")


@login_required
def dashboard(request):
    bookings = models.Booking.objects.filter(user=request.user).filter(booking_date__gte=datetime.now().date()).order_by("booking_date", "start_time")
    _unapproved_bookings = [_booking
                            for _booking in models.Booking.objects.filter(booking_date__gte=datetime.now().date())
                            if _booking.pending and _booking.is_upcoming]
    if request.method == "POST":
        if "cancel" in request.POST:
            models.Booking.objects.get(id=request.POST.get("booking_id")).delete()
        return HttpResponseRedirect(reverse("booking-dashboard"))
    return render(request, "bookings/dashboard.html", {
        "num_unapproved_bookings": len(_unapproved_bookings),
        "num_upcoming_bookings": len([_booking for _booking in bookings if _booking.approved and _booking.is_upcoming]),
        "num_pending_bookings": len([_booking for _booking in bookings if _booking.pending and _booking.is_upcoming]),
        "num_rejected_bookings": len([_booking for _booking in bookings if _booking.rejected and _booking.is_upcoming]),
        "upcoming_bookings": [_booking for _booking in bookings if _booking.approved and _booking.is_upcoming][:3]
    })


def calendar(request):
    bookings = models.Booking.objects.all()
    return render(request, "bookings/calendar.html", {
        "bookings": bookings
    })


def get_bookings(request):
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    start = dateutil.parser.parse(start) if start else start
    end = dateutil.parser.parse(end) if end else end
    bookings = models.Booking.objects.all()
    if start and end:
        bookings = bookings.filter(booking_date__gte=start).filter(booking_date__lte=end)
    elif start:
        bookings = bookings.filter(booking_date__gte=start)
    elif end:
        bookings = bookings.filter(booking_date__lte=end)

    return JsonResponse([_booking.serialize(request.user)
                         for _booking in bookings
                         if _booking.approved or (_booking.pending and _booking.is_upcoming)], safe=False)


@login_required
def my_upcoming_bookings(request):
    bookings = models.Booking.objects.filter(user=request.user).filter(booking_date__gte=datetime.now().date()).order_by("booking_date", "start_time")
    if request.method == "POST":
        if "cancel" in request.POST:
            models.Booking.objects.get(id=request.POST.get("booking_id")).delete()
        return HttpResponseRedirect(reverse("my-upcoming-bookings"))
    return render(request, "bookings/user_bookings/my_upcoming_bookings.html", {
        "upcoming_bookings": [_booking for _booking in bookings if _booking.approved and _booking.is_upcoming]
    })


@login_required
def my_pending_bookings(request):
    bookings = models.Booking.objects.filter(user=request.user).filter(booking_date__gte=datetime.now().date()).order_by("booking_date", "start_time")
    if request.method == "POST":
        if "cancel" in request.POST:
            models.Booking.objects.get(id=request.POST.get("booking_id")).delete()
        return HttpResponseRedirect(reverse("my-pending-bookings"))
    return render(request, "bookings/user_bookings/my_pending_bookings.html", {
        "pending_bookings": [_booking for _booking in bookings if _booking.pending and _booking.is_upcoming]
    })


@login_required
def my_rejected_bookings(request):
    bookings = models.Booking.objects.filter(user=request.user).filter(booking_date__gte=datetime.now().date()).order_by("booking_date", "start_time")
    return render(request, "bookings/user_bookings/my_rejected_bookings.html", {
        "rejected_bookings": [_booking for _booking in bookings if _booking.rejected and _booking.is_upcoming]
    })


@login_required
def my_past_bookings(request):
    bookings = models.Booking.objects.filter(user=request.user).filter(booking_date__lte=datetime.now().date()).order_by("-booking_date", "-start_time")
    return render(request, "bookings/user_bookings/my_past_bookings.html", {
        "past_bookings": [_booking for _booking in bookings if _booking.is_past]
    })


@staff_member_required
def unapproved_bookings(request):
    bookings = models.Booking.objects.all().filter(booking_date__gte=datetime.now().date()).order_by("booking_date", "start_time")
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
    return render(request, "bookings/all_bookings/unapproved_bookings.html", {
        "unapproved_bookings": [_booking for _booking in bookings if _booking.pending and _booking.is_upcoming],
        "approval_form": approval_form
    })


@staff_member_required
def approved_bookings(request):
    bookings = models.Booking.objects.all().filter(booking_date__gte=datetime.now().date()).order_by("booking_date", "start_time")
    approval_form = forms.ApprovalForm()
    if request.method == "POST":
        approve = "approve" in request.POST
        approval_form = forms.ApprovalForm(request.POST, approved=approve, admin=request.user,
                                           booking=models.Booking.objects.get(id=request.POST.get("booking_id")))
        if approval_form.is_valid():
            approval_form.save()
            return HttpResponseRedirect(reverse("approved-bookings"))
    return render(request, "bookings/all_bookings/approved_bookings.html", {
        "approved_bookings": [_booking for _booking in bookings if _booking.approved and _booking.is_upcoming],
        "approval_form": approval_form
    })


@staff_member_required
def rejected_bookings(request):
    bookings = models.Booking.objects.all().filter(booking_date__gte=datetime.now().date()).order_by("booking_date", "start_time")
    approval_form = forms.ApprovalForm()
    if request.method == "POST":
        approve = "approve" in request.POST
        approval_form = forms.ApprovalForm(request.POST, approved=approve, admin=request.user,
                                           booking=models.Booking.objects.get(id=request.POST.get("booking_id")))
        if approval_form.is_valid():
            approval_form.save()
            return HttpResponseRedirect(reverse("rejected-bookings"))
    return render(request, "bookings/all_bookings/rejected_bookings.html", {
        "rejected_bookings": [_booking for _booking in bookings if _booking.rejected and _booking.is_upcoming],
        "approval_form": approval_form
    })


@staff_member_required
def past_bookings(request):
    bookings = models.Booking.objects.all().filter(booking_date__lte=datetime.now().date()).order_by("-booking_date", "-start_time")
    return render(request, "bookings/all_bookings/past_bookings.html", {
        "past_bookings": [_booking for _booking in bookings if _booking.is_past]
    })


# @login_required
# def booking(request, pk):
#     return render(request, "bookings/booking.html", {
#         "booking": models.Booking.objects.get(pk=pk)
#     })


@login_required
def make_booking(request):
    if request.method == "POST":
        form = forms.BookingForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("my-pending-bookings"))
    else:
        initial = {}
        if all(param in request.GET for param in ("booking_date", "start_time", "end_time")):
            initial["booking_date"] = datetime.strptime(request.GET["booking_date"], "%m/%d/%Y")
            initial["start_time"] = datetime.strptime(request.GET["start_time"], "%H:%M")
            initial["end_time"] = datetime.strptime(request.GET["end_time"], "%H:%M")
        form = forms.BookingForm(initial=initial)
    return render(request, "bookings/make_booking.html", {
        "form": form
    })
