from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import datetime as dt

from .models import YourGoal, Outgoings, MoneyBox, Obligations
from accounts.forms import AddGoalForm, \
    AddOutgoingForm, \
    AddMoneyBoxForm, \
    AddObligationForm


# Redirecting logged user to the summary page after enter homepage.
def home(request):
    if request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/summary/')
    else:
        return render(request, 'home.html')


# Below all form to add goal/outgoings/money into a monebox/ monethy obligations
@login_required(login_url='/accounts/login')
def your_goal(request):
    goal_display = YourGoal.objects.filter(user=request.user).latest('id')
    if request.method == 'POST':
        form = AddGoalForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('/')
    else:
        form = AddGoalForm()

    return render(request, 'goal.html', context={'form': form, 'goal_display': goal_display})


@login_required(login_url='/accounts/login')
def your_outgoings(request):
    outgoings_display = Outgoings.objects.filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        form = AddOutgoingForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('/')
    else:
        form = AddOutgoingForm()

    context = {'form': form, 'outgoings_display': outgoings_display}
    return render(request, 'outgoings.html', context)


@login_required(login_url='/accounts/login')
def your_moneybox(request):
    moneybox_display = MoneyBox.objects.filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        form = AddMoneyBoxForm(request.POST)
        if form.is_valid:
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('/')
    else:
        form = AddMoneyBoxForm()

    context = {'form': form, 'moneybox_display': moneybox_display}
    return render(request, 'moneybox.html', context)


@login_required(login_url='/accounts/login')
def your_obligations(request):
    obligations_display = Obligations.objects.filter(user=request.user).order_by('-date')
    if request.method == 'POST':
        form = AddObligationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('http://127.0.0.1:8000/summary/')
    else:
        form = AddObligationForm

    context = {'form': form, 'obligations_display': obligations_display}
    return render(request, 'obligations.html', context)


# Summary page with data to view for user with a little history look.
@login_required(login_url='/accounts/login')
def account_summary(request):
    last_30 = dt.date.today() - dt.timedelta(days=30)

    goal_display = YourGoal.objects.filter(user=request.user).latest('id')
    outgoings_display = Outgoings.objects.filter(user=request.user).order_by('-date')[:3]
    piggybank_sum_display = MoneyBox.objects.filter(user=request.user).aggregate(Sum('suma'))['suma__sum']
    obligations_display = Obligations.objects.filter(user=request.user).order_by('-date')[:3]
    outgoings_sum_display = Outgoings.objects.filter(user=request.user, date__gt=last_30).aggregate(Sum('suma'))['suma__sum']
    obligations_sum_display = Obligations.objects.filter(user=request.user).aggregate(Sum('suma'))['suma__sum']
    goal = goal_display
    outgoings = outgoings_display
    piggybank = piggybank_sum_display
    obligations = obligations_display

    context = {'goal': goal,
               'outgoings': outgoings,
               'piggybank': piggybank,
               'obligations': obligations,
               'outgoings_sum_display': outgoings_sum_display,
               'obligations_sum_display': obligations_sum_display}

    return render(request, 'summary.html', context)
