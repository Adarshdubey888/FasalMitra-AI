from django.shortcuts import render, redirect
from .models import Farmer
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from twilio.rest import Client
import os


# Admin Login

def admin_login(request):

    error = None

    if request.method == "POST":

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(

            request,
            username=username,
            password=password
        )

        if user is not None and user.is_superuser:

            request.session.flush()

            login(request, user)

            return redirect('/admin-dashboard/')

        else:

            error = "Invalid Admin Credentials"

    return render(request, 'admin_login.html', {

        'error': error
    })


# Register View

def register(request):

    if request.method == "POST":

        name = request.POST.get('name')

        phone = request.POST.get('phone')

        village = request.POST.get('village')

        state = request.POST.get('state')

        otp = random.randint(1000, 9999)

        request.session['name'] = name

        request.session['phone'] = phone

        request.session['village'] = village

        request.session['state'] = state

        request.session['otp'] = str(otp)

        request.session['demo_otp'] = otp

        return render(request, 'verify_otp.html', {

            'demo_otp': otp
        })

    return render(request, 'register.html')


# OTP Verification

def verify_otp(request):

    if request.method == "POST":

        entered_otp = request.POST.get('otp')

        real_otp = request.session.get('otp')

        if entered_otp == real_otp:

            Farmer.objects.get_or_create(

                phone=request.session.get('phone'),

                defaults={

                    'name': request.session.get('name'),

                    'village': request.session.get('village'),

                    'state': request.session.get('state')
                }
            )

            return redirect('/login/')

    return render(request, 'verify_otp.html')


# Login

def login_user(request):

    if request.method == "POST":

        phone = request.POST.get('phone')

        farmer = Farmer.objects.filter(phone=phone).first()

        if farmer:

            otp = random.randint(1000, 9999)

            request.session['login_phone'] = phone

            request.session['login_otp'] = str(otp)

            return render(request, 'login_otp.html', {

                'demo_otp': otp
            })

    return render(request, 'login.html')


# Verify Login OTP

def login_otp(request):

    if request.method == "POST":

        entered_otp = request.POST.get('otp')

        real_otp = request.session.get('login_otp')

        if entered_otp == real_otp:

            request.session['farmer_phone'] = request.session.get('login_phone')

            return redirect('/')

    return render(request, 'login_otp.html')


# Logout

def logout_user(request):

    request.session.flush()

    return redirect('home')


# Profile

def profile(request):

    phone = request.session.get('farmer_phone')

    farmer = Farmer.objects.get(phone=phone)

    context = {

        'farmer': farmer
    }

    return render(request, 'profile.html', context)


# Admin Dashboard

@login_required
def admin_dashboard(request):

    return render(request, 'admin_dashboard.html')