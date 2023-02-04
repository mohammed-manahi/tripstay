from django.db import models
from location_field.models.plain import PlainLocationField
from django.conf import settings
from django.utils.text import slugify


class Property(models.Model):
    """
    Create property model
    """
    FREE_CANCELLATION = 'Free Cancellation'
    PAID_CANCELLATION = 'Paid Cancellation'
    CANCELLATION_POLICY_CHOICES = [
        (FREE_CANCELLATION, FREE_CANCELLATION),
        (PAID_CANCELLATION, PAID_CANCELLATION)
    ]
    name = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=250, blank=True)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    address = models.CharField(max_length=250)
    # Use third-party library location field for property location
    location = PlainLocationField(based_fields=['city'], zoom=7)
    number_of_bedrooms = models.PositiveSmallIntegerField()
    number_of_beds = models.PositiveSmallIntegerField()
    number_of_baths = models.PositiveSmallIntegerField()
    capacity_for_adults = models.PositiveSmallIntegerField()
    capacity_for_children = models.PositiveSmallIntegerField()
    available = models.BooleanField()
    available_from = models.DateTimeField()
    available_to = models.DateTimeField()
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    cancellation_policy = models.CharField(max_length=50, choices=CANCELLATION_POLICY_CHOICES,
                                           default=FREE_CANCELLATION)
    cancellation_fee = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta():
        # Define meta attributes
        ordering = ['-created_at']
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    def save(self, *args, **kwargs):
        # Override save method to automatically assign the slug field based on the property name using slugify
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name