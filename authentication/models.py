from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **other_entries):
        # Other entries should contain the First Name, Last Name and the
        if not email:
            raise serializers.ValidationError(_('Please enter an email address'))

        email = self.normalize_email(email)
        new_user = self.model(email=email, **other_entries)

        new_user.set_password(password)
        
        # Save the instance
        new_user.save()

        return new_user

    def create_superuser(self, email, password, **other_entries):
        other_entries.setdefault('is_staff', True)
        other_entries.setdefault('is_superuser', True)
        other_entries.setdefault('is_active', True)

        if not other_entries.get('is_staff'):
            return ValueError(_('Super user should have is_staff as True'))

        if not other_entries.get('is_superuser'):
            return ValueError(_('Super user should have is_superuser as True'))

        if not other_entries.get('is_active'):
            return ValueError(_('Super user should have is_active as True'))

        return self.create_user(email, password, **other_entries)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=80, unique=True)
    last_name = models.CharField(max_length=25)
    first_name = models.CharField(max_length=25)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}->{self.first_name}'

#
# class TokenAuthentication(TokenAuthentication):
#     keyword = 'Bearer'
