from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from functools import partial

from savings.models import *


# User register form with email added.
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class HolderForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image', ]


# Below all form to add goal/outgoings/money into a monebox/ monethy obligations.
class AddGoalForm(forms.ModelForm):

    class Meta:
        model = YourGoal
        exclude = ['user', 'date', ]


class AddOutgoingForm(forms.ModelForm):

    class Meta:
        model = Outgoings
        exclude = ['user', 'date', ]


class AddMoneyBoxForm(forms.ModelForm):

    class Meta:
        model = MoneyBox
        exclude = ['user', 'date', ]


class AddObligationForm(forms.ModelForm):

    class Meta:
        model = Obligations
        exclude = ['user', 'date', ]


# Form to pick a date range to filter history of added goal/outgoings/obligations and moneybox.
DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class PickADate(forms.Form):
    date_from = forms.DateField(widget=DateInput())
    date_to = forms.DateField(widget=DateInput())

