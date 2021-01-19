from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver

from MyOne import settings


class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    subject = models.TextField(default='')
    message = models.TextField(default='')

    def __str__(self):
        return self.name


class User_Register(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    password1 = models.TextField(default='')
    password2 = models.TextField(default='')

    def __str__(self):
        return self.username


class User_Profile(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male',),
        ('F', 'Female',),
        ('O', 'Other',),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    tel = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, )
    birth_date = models.DateField(null=True, blank=True)
    img = models.ImageField(upload_to=settings.MEDIA_ROOT, null=True, blank=True)
    prof = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User_Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100,default="")
    subcategory = models.CharField(max_length=100,default="")
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    date = models.DateField()
    image = models.ImageField(upload_to=settings.MEDIA_ROOT, null=True, blank=True)

    def __str__(self):
        return self.product_name
