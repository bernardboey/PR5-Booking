# Generated by Django 3.0.8 on 2020-07-25 09:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookings', '0002_auto_20200719_0055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='equipment_used',
        ),
        migrations.AddField(
            model_name='approval',
            name='booking',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approvals', to='bookings.Booking'),
        ),
        migrations.AddField(
            model_name='booking',
            name='acoustic_guitar_amp',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='bass_amp',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='drums',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='electric_guitar_amps',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='keyboard',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='microphones',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='mixer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='approval',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings_reviewed', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='booking',
            name='number_of_external_users',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='booking',
            name='number_of_yale_nus_users',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)]),
        ),
        migrations.AlterField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to=settings.AUTH_USER_MODEL),
        ),
    ]