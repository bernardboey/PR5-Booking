from django import forms

from . import models


EQUIPMENT_CHOICES = (
    ("mixer", "Mixer"),
    ("microphones", "Microphones"),
    ("drums", "Drums"),
    ("keyboard", "Keyboard"),
    ("bass_amp", "Bass Amp"),
    ("acoustic_guitar_amp", "Acoustic Guitar Amp"),
    ("electric_guitar_amps", "Electric Guitar Amps"),
)

EQUIPMENT_CHOICES = ((equipment.name, equipment.verbose_name) for equipment in models.Booking.EQUIPMENT)


class BookingForm(forms.ModelForm):
    required_css_class = "required"

    equipment_used = forms.MultipleChoiceField(choices=EQUIPMENT_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
        "class": "custom-control-input"
    }))

    class Meta:
        model = models.Booking
        fields = ("booking_date", "start_time", "end_time", "purpose", "group_name", "comments",
                  "number_of_external_users", "number_of_yale_nus_users")
        widgets = {
            "number_of_yale_nus_users": forms.Select(
                choices=((i, i) for i in range(1, models.Booking.MAX_YALE_NUS_USERS + 1))),
            "number_of_external_users": forms.Select(
                choices=((i, i) for i in range(0, models.Booking.MAX_EXTERNAL_USERS + 1))),
            "booking_date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        if user:
            self.instance.user = user
        equipment_used = self["equipment_used"].value() or []
        for equipment in equipment_used:
            setattr(self.instance, equipment, True)
