import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ContactForm, NewUserForm, UserForm, ProfileForm
from MyOne import settings
from django.contrib.auth.models import User
from django.db import transaction

def Home(request):
    today = datetime.datetime.now().date()
    return render(request, "index.html", {"today": today})


def Products(request):
    return render(request, "products.html", {})


def About(request):
    return render(request, "about.html", {})


def Contact(request):
    cform = ContactForm(request.POST)
    if request.method == 'POST':
        if cform.is_valid():
            contact_name = cform.cleaned_data['name']
            contact_email = cform.cleaned_data['email']
            print(contact_email)
            subject = cform.cleaned_data['subject']
            message = cform.cleaned_data['message']
            cform.save()
            email_from = contact_email
            email_to = [settings.EMAIL_HOST_USER, ]
            send_mail(subject, message, email_from, email_to)
            return render(request, 'msg1.html',
                          {'title': subject, 'content': 'We got your message.We will get back to you soon.'})
        else:
            cform = ContactForm()
    template = 'contact.html'
    return render(request, template, {'form': cform})


def Profile(request):
    template = 'profile.html'
    return render(request, template, {})


def Login(request):
    if request.method == 'POST':

        username = request.POST.get('email')
        print(username)

        password = request.POST.get('pass')
        print(password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('/home')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})


def Register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/home')

    form = NewUserForm
    return render(request=request, template_name="register.html", context={"register_form": form})


def Logout(request):
    logout(request)
    return redirect('/home')


@login_required
@transaction.atomic
def EditProfile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST or None, request.FILES or None, instance=request.user)
        profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profileform.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
#
#
# DeleteView
@login_required
def deleteProfile(request, pk):
    template = 'profiledelete.html'
    profile = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('home')
    return render(request, template, {'object': profile})
