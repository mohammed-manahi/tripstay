from django.db import models
from location_field.models.plain import PlainLocationField
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from property.validators import validate_image_size, validate_video_size


class PropertyCategory(models.Model):
    """
    Create property category model and associate it with one-to-many relationship with property model
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta():
        ordering = ['-created_at']
        verbose_name = 'Property Category'
        verbose_name_plural = 'Property Categories'

    def save(self, *args, **kwargs):
        # Override save method to automatically assign the slug field based on the property name using slugify
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Property(models.Model):
    """
    Create property model
    """
    name = models.CharField(max_length=250, blank=False)
    description = models.TextField(max_length=500)
    slug = models.SlugField(max_length=250, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties_owned')
    category = models.ForeignKey(PropertyCategory, on_delete=models.CASCADE, related_name='properties')
    address = models.CharField(max_length=250)
    # Use third-party library location field for property location
    location = PlainLocationField(based_fields=['city'], zoom=7)
    number_of_bedrooms = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    number_of_beds = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    number_of_baths = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    capacity_for_adults = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    capacity_for_children = models.PositiveSmallIntegerField()
    available = models.BooleanField()
    available_from = models.DateTimeField()
    available_to = models.DateTimeField()
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


class PropertyMedia(models.Model):
    """
    Create property media model and associate it with many-to-one relationship with property model
    """
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_media')
    photo = models.ImageField(upload_to='property/photos',
                              validators=[validate_image_size, FileExtensionValidator(['jpg', 'png', 'jpeg'])])
    video = models.FileField(upload_to='property/videos', validators=[validate_video_size, FileExtensionValidator(
        ['mp4', 'webm', 'mkv', 'flv', 'wmv'])])

    class Meta():
        verbose_name = 'Property Media'
        verbose_name_plural = 'Property Media'

    def __str__(self):
        return self.name


class PropertyReview(models.Model):
    """
    Create property review model and associate it with many-to-one relationship with property model
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_reviews')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_reviews')
    comment = models.TextField(blank=True)
    rate = models.FloatField(blank=True, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta():
        ordering = ['-created_at']
        verbose_name = 'Property Review'
        verbose_name_plural = 'Property Reviews'

    def total_reviews(self):
        return self.comment.count()

    def __str__(self):
        return self.comment


class PropertyFeatureCategory(models.Model):
    """
    Create property feature category model and associate it with one-to-many relationship with property feature model
    """
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True)

    class Meta():
        verbose_name = 'Property Feature Category'
        verbose_name_plural = 'Property Feature Categories'

    def save(self, *args, **kwargs):
        # Override save method to automatically assign the slug field based on the property name using slugify
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PropertyFeature(models.Model):
    """
    Create property feature model and associate it with many-to-one relationship with property model
    """
    name = models.CharField(max_length=250, blank=False)
    description = models.TextField(blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='features')
    feature_category = models.ForeignKey(PropertyFeatureCategory, on_delete=models.CASCADE,
                                         related_name='property_features')

    class Meta():
        verbose_name = 'Property Feature'
        verbose_name_plural = 'Property Features'

    def __str__(self):
        return self.name
