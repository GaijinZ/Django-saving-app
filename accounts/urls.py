from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('outgoings_history/', views.outgoings_history, name='outgoings_history'),
    path('obligations_history/', views.obligations_history, name='obligations_history'),
    path('your_goal_history/', views.your_goal_history, name='your_goal_history'),
    path('moneybox_history/', views.moneybox_history, name='moneybox_history')
]
