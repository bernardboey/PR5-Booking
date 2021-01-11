from django.db import models
from django.contrib.postgres import fields
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

from datetime import datetime


class Booking(models.Model):
    MAX_YALE_NUS_USERS = 5
    MAX_EXTERNAL_USERS = 0

    timestamp = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    booking_date = models.DateField("Booking Date")
    start_time = models.TimeField("Start Time")
    end_time = models.TimeField("End Time")
    purpose = models.CharField(max_length=40)
    group_name = models.CharField("Group Name", max_length=40, blank=True)
    comments = models.CharField(max_length=200, blank=True)
    number_of_yale_nus_users = models.PositiveSmallIntegerField("No. of Yale-NUS Users",
                                                                validators=[MinValueValidator(1),
                                                                            MaxValueValidator(MAX_YALE_NUS_USERS)])
    number_of_external_users = models.PositiveSmallIntegerField("No. of External Users",
                                                                validators=[MaxValueValidator(MAX_EXTERNAL_USERS)])
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="bookings")
    mixer = models.BooleanField("Mixer", default=False)
    microphones = models.BooleanField("Microphones", default=False)
    drums = models.BooleanField("Drums", default=False)
    keyboard = models.BooleanField("Keyboard", default=False)
    bass_amp = models.BooleanField("Bass Amp", default=False)
    acoustic_guitar_amp = models.BooleanField("Acoustic Guitar Amp", default=False)
    electric_guitar_amps = models.BooleanField("Electric Guitar Amps", default=False)

    EQUIPMENT = (mixer, microphones, drums, keyboard, bass_amp, acoustic_guitar_amp, electric_guitar_amps)

    @cached_property
    def equipment_used(self):
        return ", ".join([equipment.verbose_name for equipment in Booking.EQUIPMENT if getattr(self, equipment.name)])

    @cached_property
    def status(self):
        if self.approved:
            return "Approved"
        elif self.rejected:
            return "Rejected"
        else:
            return "Pending"

    @cached_property
    def approval(self):
        try:
            return self.approvals.latest("timestamp")
        except Approval.DoesNotExist:
            return None

    @cached_property
    def approved(self):
        if approval := self.approval:
            return approval.approved

    @cached_property
    def rejected(self):
        if approval := self.approval:
            return not approval.approved

    @cached_property
    def pending(self):
        return self.approval is None

    @cached_property
    def is_upcoming(self):
        today = datetime.now().date()
        return self.booking_date > today or self.booking_date == today and self.end_time >= datetime.now().time()

    @cached_property
    def is_past(self):
        return not self.is_upcoming

    def clean(self, *args, **kwargs):
        if self.end_time <= self.start_time:
            raise ValidationError({"end_time": ["End Time must be later than Start Time"]})
        clashed_bookings = Booking.objects.filter(booking_date=self.booking_date).filter(end_time__gt=self.start_time).filter(start_time__lt=self.end_time)
        clashed_bookings = [booking for booking in clashed_bookings if (booking.approved or (booking.pending and booking.is_upcoming)) and booking.pk != self.pk]
        if clashed_bookings:
            raise ValidationError("Selected date and time clashes with existing booking")
        if not (self.mixer or self.drums or self.keyboard or self.microphones
                or self.bass_amp or self.acoustic_guitar_amp or self.electric_guitar_amps):
            raise ValidationError({"equipment_used": ["Please select at least one."]})

    def serialize(self, user):
        return {
            "title": ("[Pending] " if self.pending else "") + self.user.name + f" ({self.purpose})",
            "start": self.booking_date.strftime("%Y-%m-%d") + self.start_time.strftime("T%H:%M:%S"),
            "end": self.booking_date.strftime("%Y-%m-%d") + self.end_time.strftime("T%H:%M:%S"),
            "color": ("#ff9e60" if self.user == user else "#ffe859") if self.pending else ("#28a745" if self.user == user else "#3788d8"),
            "textColor": "#000000" if self.pending else "#FFFFFF"
        }


class Approval(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="approvals", null=True)
    comments_for_user = models.CharField(max_length=200, blank=True)  # "Auto-approved" if booking by an admin
    comments_for_admin = models.CharField(max_length=200, blank=True)  # "Auto-approved" if booking by an admin
    admin = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="bookings_reviewed")
    approved = models.BooleanField()
