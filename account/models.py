from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """
    Customize base user manager to normalize email field and encrypt password field
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save regular user with a given email and password
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a superuser with a given email and password
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser, PermissionsMixin):
    """
    Customize default django authentication user model by inheriting abstract user
    """
    HOST = 'host'
    GUEST = 'guest'
    STAFF = 'staff'
    ADMIN = 'admin'
    USER_ROLE = [
        (HOST, HOST),
        (GUEST, GUEST),
        (STAFF, STAFF),
        (ADMIN, ADMIN),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    role = models.CharField(max_length=10, choices=USER_ROLE, default=GUEST)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # Set username field to email for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    def get_role(self):
        return self.role

    def __str__(self):
        return self.email
