from django.contrib import admin
from account.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Register customized user model in admin site
    """
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                # Add user fields to default user model
                "fields": ('email', 'first_name', 'last_name', 'role', 'password', 'username'),
            },
        ),
    )
