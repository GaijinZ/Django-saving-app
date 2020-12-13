from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from functools import partial

from savings.models import YourGoal
from savings.models import Outgoings
from savings.models import MoneyBox
from savings.models import Obligations


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


DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class PickADate(forms.Form):
    date_from = forms.DateField(widget=DateInput())
    date_to = forms.DateField(widget=DateInput())

