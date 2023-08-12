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
    path('list-of-vans', list_of_vans, name='list_of_vans'),
    path('rent-a-van', rent_van, name='rent_van'),
    path('rent-booking', rent_booking_list, name='rent_booking_list'),
    path('confirmed-booking', confirmed_bookings, name='confirmed_bookings'),
    path('past-booking', past_booking, name='past_booking'),
    path('rejected-booking', rejected_booking, name='rejected_booking'),
    path('pending-booking', pending_booking, name='pending_booking'),
    path('cancelled-booking', cancelled_booking, name='cancelled_booking'),

    path('rent-a-van/<id>/', rent_a_van, name='rent_a_van'),
    path('open/notification/<id>/', open_notification, name='open_notification'),
    path('approve-pending-driver/<id>/', approve_pending_driver, name='approve_pending_driver'),
    path('pending-driver-info/<id>/', get_pending_driver_info, name='get_pending_driver_info'),
    path('get-address-destination/<id>/', get_destination_address, name='get_destination_address'),

    path('test', add_municipality, name='add_municipality'),
]