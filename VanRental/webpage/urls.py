from django.urls import path
from django.urls import path,include
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('index', index, name='index'),
    path('login', login_page, name='login_page'),
    path('signup', signup_page, name='signup_page'),
    path('logout', logout_page, name='logout_page'),
    path('logout', logout_page, name='logout_page'),
    path('verify/<account_type>/<auth_token>', verify, name='verify'),
    path('profile', profile, name='profile'),
    path('pending-drivers', pending_drivers, name='pending_drivers'),
    path('approve-pending-driver/<id>/', approve_pending_driver, name='approve_pending_driver'),

]