from django.contrib import admin
from .models import Booking
from .models import Approval

admin.site.register(Booking)
admin.site.register(Approval)
