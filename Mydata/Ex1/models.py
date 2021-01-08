import os
import random

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    subject = models.TextField(default='')
    message = models.TextField(default='')

    def __str__(self):
        return self.name


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 1000)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "users/{final_filename}".format(final_filename=final_filename)


class Profile(models.Model):
    phone_regex = RegexValidator(regex=r'^+?1?d{9,15}$',
                                 message="Enter valid phone number must be entered in the format: '+9999999999'.")
    GENDER_CHOICES = (
        ('M', 'Male',),
        ('F', 'Female',),
        ('O', 'Other',),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    tel = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, )
    birth_date = models.DateField(null=True, blank=True)
    img = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    def __str__(self):
        return self.user
