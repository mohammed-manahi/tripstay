from django.contrib import admin
from property.models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    """
    Register property model in admin site
    """
    pass
