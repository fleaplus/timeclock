from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.core.mail import send_mail


class TimeclockUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class TimeclockUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email_address',
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=True)

    objects = TimeclockUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_superuser
