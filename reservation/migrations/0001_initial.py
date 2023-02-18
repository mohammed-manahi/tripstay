# Generated by Django 4.1.6 on 2023-02-18 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('property', '0007_property_cancellation_fee_per_night_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_from', models.DateTimeField()),
                ('reservation_to', models.DateTimeField()),
                ('guest', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reservation', to=settings.AUTH_USER_MODEL)),
                ('property', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reservation', to='property.property')),
            ],
            options={
                'verbose_name': 'Reservation',
                'verbose_name_plural': 'Reservations',
            },
        ),
    ]
