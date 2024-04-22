from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.validators import MaxValueValidator, RegexValidator
import os


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone is required")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        user = self.create_user(phone, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if password is None:
            raise TypeError("Password cannot be empty")

        return user


def uploadUserPic(instance, filename):
    fileExtention = filename.split(".")[-1]
    newFileName = f"user_{instance.phone}.{fileExtention}"
    return os.path.join('profile_pic', newFileName)


class User(AbstractBaseUser, PermissionsMixin):
    fullName = models.CharField(max_length=255)
    phone = models.CharField(
        max_length=10, unique=True, db_index=True, validators=[RegexValidator(r'^[0-9]{10}$', message="Phone number must be 10 digits")])
    # email = models.EmailField(max_length=100,blank=True)
    # profilePic = models.ImageField(
    #     upload_to=uploadUserPic, blank=True, null=True)
    companyName = models.CharField(max_length=255, validators=[RegexValidator(
        r'^[a-zA-Z0-9 ]{5,100}$', message="Company name not valid")])
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    objects = CustomUserManager()

    def __str__(self):
        return self.fullName



class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=255)
    startDate = models.DateField(default=timezone.now().date())
    endDate = models.DateField(default=timezone.now().date())

    def get_endDate(self):
        return self.endDate

    def get_states(self):
        return self.state
