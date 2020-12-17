from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime as dt
from itertools import chain
from django.db.models import Q

from .forms import NewUserForm, PickADate, HolderForm
from savings.models import *


# Create your views here.
def logout_request(request):
    logout(request)
    messages.info(request, 'Zostaleś wylogowany')
    return redirect('/')


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Jesteś zalogowany jako {username}')
                return redirect('http://127.0.0.1:8000/summary/')
            else:
                messages.error(request, 'Nie prawidłowa nazwa użytkownika lub hasło')

    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Konto stworzone {username}')
            login(request, user)
            messages.info(request, f'Jesteś zalogowany jako {username}')
            return redirect('/')
        else:
            for msg in form.error_messages:
                messages.error(request, f'Błąd { msg }')

    form = NewUserForm
    return render(request, 'register.html',
                  context={'form': form})


@login_required(login_url='/accounts/login')
def profile(request):
    form = HolderForm(instance=request.user)
    if request.method == 'POST':
        form = HolderForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            user_img = form.save(commit=False)
            user_img.user = request.user
            user_img.image = request.FILES['image']
            user_img.save()

    context = {'form': form}
    return render(request, 'profile.html', context)


# Functions below full history look with dates range to view.
@login_required(login_url='/accounts/login')
def outgoings_history(request):
    last_30 = dt.date.today() - dt.timedelta(days=30)
    search_result = Outgoings.objects.filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        form = PickADate(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            search_result = search_result.filter(date__range=(date_from, date_to))
            return render(request, 'outgoings_history.html', {'data': search_result})

    display_data = Outgoings.objects.filter(user=request.user, date__gt=last_30).order_by('-date')
    return render(request, 'outgoings_history.html', {'data': display_data})


@login_required(login_url='/accounts/login')
def obligations_history(request):
    search_result = Obligations.objects.filter(user=request.user).order_by('-date')
    if request.method == "POST":
        form = PickADate(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            search_result = search_result.filter(date__range=(date_from, date_to))
            return render(request, 'obligations_history.html', {'data': search_result})

    display_data = Obligations.objects.filter(user=request.user).order_by('-date')[:10]
    return render(request, 'obligations_history.html', {'data': display_data})


@login_required(login_url='/accounts/login')
def your_goal_history(request):
    search_result = YourGoal.objects.filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        form = PickADate(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            search_result = search_result.filter(date__range=(date_from, date_to))
            return render(request, 'your_goal_history.html', {'data': search_result})

    display_data = YourGoal.objects.filter(user=request.user).order_by('-date')
    return render(request, 'your_goal_history.html', {'data': display_data})


@login_required(login_url='/accounts/login')
def moneybox_history(request):
    search_result = MoneyBox.objects.filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        form = PickADate(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            search_result = search_result.filter(date__range=(date_from, date_to))
            return render(request, 'moneybox_history.html', {'data': search_result})

    display_data = MoneyBox.objects.filter(user=request.user).order_by('-date')
    return render(request, 'moneybox_history.html', {'data': display_data})


