from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.


class CustomUserManager(BaseUserManager):

    def create_user(self, email=None, password=None, **kwargs):

        if not email:
            raise ValueError("You have to provide your email address")

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email=None, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        user = self.create_user(email, password, **kwargs)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom class that respresents a User of our app"""

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(default=timezone.now, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def full_name(self):
        """Get the full name of user on base of first and last name

        Returns:
            str: full name
        """
        return f"{self.first_name} {self.last_name}"


class Participant(models.Model):
    """
    Represents an individual who participates in polls, identified by their IP address.
    """

    ip_address = models.CharField(max_length=15, unique=True)

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True)
