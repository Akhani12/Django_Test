from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm, UserForm, ProfileForm, regiform
from MyOne import settings
from django.contrib.auth.models import User
from django.db import transaction


def Home(request):
    return render(request, "index.html", {})


def Products(request):
    return render(request, "products.html", {})


def About(request):
    return render(request, "about.html", {})


def Contact(request):
    cform = ContactForm(request.POST)
    if request.method == 'POST':
        if cform.is_valid():
            contact_email = cform.cleaned_data['email']
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
        rform = regiform(request.POST)
        if rform.is_valid():
            u_name = rform.cleaned_data['username']
            u_email = rform.cleaned_data['email']
            u_password = rform.cleaned_data['password1']

            User.objects.create_user(u_name, u_email, u_password)
            user = authenticate(username=u_name, password=u_password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('/home')
        messages.success(
            request,
            "You're now a user! You've been signed in, too."
        )
        print(rform.errors)

    form = regiform
    return render(request=request, template_name="register.html", context={"register_form": form})


def Logout(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return redirect('/login')


@login_required(login_url="login")
def Profile(request):
    template = 'profile.html'
    return render(request, template, {})


@login_required(login_url="login")
@transaction.atomic
def EditProfile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST or None, request.FILES or None, instance=request.user)
        profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.user_profile)
        if profile_form.is_valid():
            user_form.save(commit=True)
            profile_form.save(commit=True)

            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.user_profile)
    return render(request, 'profileform.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
