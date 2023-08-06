from django import template
from ..models import *
register = template.Library()


@register.simple_tag
def get_my_notifications(user):
    if user:
        my_notifications = Notification.objects.filter(receiver_id = user).all().order_by('-date_recorded')
        return my_notifications

@register.simple_tag
def get_my_profile(user):
    admin_account = AdminAccount.objects.filter(user_id = user).first()
    driver_account = DriverAccount.objects.filter(user_id = user).first()
    passenger_account = PassengerAccount.objects.filter(user_id = user).first()

    if admin_account:
        if admin_account.profile:
            return admin_account.profile
        else:
            return None
        
    elif driver_account:
        if driver_account.profile:
            return driver_account.profile
        else:
            return None
        
    elif passenger_account:
        if passenger_account.profile:
            return passenger_account.profile
        else:
            return None
    else:
        return None
    
        