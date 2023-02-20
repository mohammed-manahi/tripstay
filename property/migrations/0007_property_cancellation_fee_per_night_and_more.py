# Generated by Django 4.1.6 on 2023-02-18 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0006_alter_property_address_alter_property_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='cancellation_fee_per_night',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
        migrations.AddField(
            model_name='property',
            name='cancellation_policy',
            field=models.CharField(choices=[('Free Cancellation', 'Free Cancellation'), ('Paid Cancellation', 'Paid Cancellation')], default='Free Cancellation', max_length=50),
        ),
    ]