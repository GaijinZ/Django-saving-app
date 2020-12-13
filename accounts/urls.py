from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('history/', views.user_history, name='history'),
    path('outgoings_history/', views.outgoings_history, name='outgoings_history')
]
