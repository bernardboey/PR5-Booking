from django.db import models
from django.contrib.postgres import fields
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Booking(models.Model):
    MAX_YALE_NUS_USERS = 3
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

    @property
    def equipment_used(self):
        return ", ".join([equipment.verbose_name for equipment in Booking.EQUIPMENT if getattr(self, equipment.name)])

    def approved(self):
        # if no approval, say no
        return self.approvals.latest("timestamp")

    def clean(self, *args, **kwargs):
        if self.end_time <= self.start_time:
            raise ValidationError({"end_time": ["End Time must be later than Start Time"]})
        if not (self.mixer or self.drums or self.keyboard or self.microphones
                or self.bass_amp or self.acoustic_guitar_amp or self.electric_guitar_amps):
            raise ValidationError({"equipment_used": ["Please select at least one."]})


class Approval(models.Model):
    class Status(models.IntegerChoices):
        APPROVED = 1
        PENDING = 0
        REJECTED = -1
    timestamp = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="approvals", null=True)
    comments_for_user = models.CharField(max_length=200, blank=True)  # "Auto-approved" if booking by an admin
    comments_for_admin = models.CharField(max_length=200, blank=True)  # "Auto-approved" if booking by an admin
    admin = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="bookings_reviewed")
    status = models.IntegerField(choices=Status.choices)
