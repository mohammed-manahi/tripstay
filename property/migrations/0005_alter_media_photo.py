# Generated by Django 4.1.6 on 2023-02-11 14:55

import django.core.validators
from django.db import migrations, models
import property.validators


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_alter_media_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='photo',
            field=models.ImageField(blank=True, upload_to='property/photos', validators=[property.validators.validate_image_size, django.core.validators.FileExtensionValidator(['jpg', 'png', 'jpeg'])]),
        ),
    ]
