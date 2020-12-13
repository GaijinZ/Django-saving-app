from django.urls import path

from . import views

app_name = 'savings'
urlpatterns = [
    path('', views.home, name='home'),
    path('goal/', views.your_goal, name='goal'),
    path('outgoings/', views.your_outgoings, name='outgoings'),
    path('moneybox/', views.your_moneybox, name='moneybox'),
    path('obligations/', views.your_obligations, name='obligations'),
    path('summary/', views.account_summary, name='summary')
]
