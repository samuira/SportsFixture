from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        """
        Creates and saves a User with the given username, password.
        """
        if not email:
            raise ValueError('Users must have an username')
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given username and 	password.
        Apply is_superuser status is TRUE
        """
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(max_length=60, unique=True)
    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='user/profile_images/%Y/%m/%d', default='')

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(User, self).save(*args, **kwargs)
