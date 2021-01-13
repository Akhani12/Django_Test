from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from Ex1.models import Contact, User_Profile, User_Register


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']

class regiform(ModelForm):
    class Meta:
        model = User_Register
        fields = ['username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileForm(ModelForm):
    class Meta:
        birth_date = forms.DateField(input_formats=['%d, %B, %Y'])
        model = User_Profile
        fields = ['bio', 'location', 'tel', 'gender', 'birth_date', 'img','prof']
