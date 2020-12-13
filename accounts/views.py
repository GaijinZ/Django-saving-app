from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import ExtractWeek

from .forms import NewUserForm, PickADate
from savings.models import YourGoal, Outgoings, Obligations, MoneyBox


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
    return render(request, 'profile.html')


@login_required(login_url='/accounts/login')
def user_history(request):
    if request.method == 'POST':
        form = PickADate(request.POST)
        if form.is_valid():
            datef = request.POST.get['datef']
            datet = request.POST.get['datet']
            try:
                t = Outgoings.objects.filter(user=request.user, date__lte=datet, date__gte=datef)
            except:
                t = None
            return render(request, 'history.html', {'t': t})
    else:
        form = PickADate()

    goal_history = YourGoal.objects.filter(user=request.user).order_by('date')

    outgoings_history = Outgoings.objects.filter(user=request.user) \
        .annotate(tydzien=ExtractWeek('date')) \
        .values('tydzien') \
        .annotate(razem=Sum('suma')) \
        .order_by('tydzien')

    obligations_history = Obligations.objects.filter(user=request.user) \
        .annotate(tydzien=ExtractWeek('date')) \
        .values('tydzien') \
        .annotate(razem=Sum('kwota')) \
        .order_by('tydzien')

    moneybox_history = MoneyBox.objects.filter(user=request.user) \
        .annotate(tydzien=ExtractWeek('date')) \
        .values('tydzien') \
        .annotate(razem=Sum('wolumen')) \
        .order_by('tydzien')

    context = {'goal_history': goal_history,
               'outgoings_history': outgoings_history,
               'obligations_history': obligations_history,
               'moneybox_history': moneybox_history,
               'form': form}

    return render(request, 'history.html', context)


@login_required(login_url='/accounts/login')
def outgoings_history(request):
    search_result = Outgoings.objects.filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        form = PickADate(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            search_result = search_result.filter(date__range=(date_from, date_to))
    else:
        displaydata = Outgoings.objects.filter(user=request.user).order_by('-date')
        return render(request, 'outgoings_history.html', {'data': displaydata})
