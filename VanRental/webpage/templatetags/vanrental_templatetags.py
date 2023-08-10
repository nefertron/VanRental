from django import template
from ..models import *
from django.db.models import Q


register = template.Library()

@register.simple_tag
def user_type_checker(user):
    if user:
        if AdminAccount.objects.filter(user_id = user).first():
            return 'Admin'
        
        elif DriverAccount.objects.filter(user_id = user).first():
            return 'Driver'
        
        elif PassengerAccount.objects.filter(user_id = user).first():
            return 'Passenger'
        else:
            return None
    else:
        return None

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
    

@register.simple_tag
def get_all_van_images(van):
    all_images = VanImages.objects.filter(van_image_id = van).all()
    return all_images


@register.simple_tag
def all_van_images_indices(van):
    all_images = VanImages.objects.filter(van_image_id = van).count()
    indexes = []

    for i in range(0, all_images):
        indexes.append(i)

    return indexes


@register.simple_tag
def get_van_total_rental_and_carpool_service(van):
    all_services = []

    all_rented_services = RentedVan.objects.filter(plate_no = van, is_done = True).count()
    if all_rented_services == None:
        all_services.append(0)
    else:
        all_services.append(all_rented_services)

    all_carpooled_services = CarpoolVan.objects.filter(plate_no = van, is_done = True).count()
    if all_carpooled_services == None:
        all_services.append(0)
    else:
        all_services.append(all_carpooled_services)

    return all_services


@register.simple_tag
def get_rent_vans():
    all_to_rent_vans = Van.objects.filter(is_carpooled = False).all()

    return all_to_rent_vans


@register.simple_tag
def get_carpool_vans():
    all_to_carpool_vans = Van.objects.filter(is_carpooled = True).all()

    return all_to_carpool_vans



@register.simple_tag
def get_all_rented():
    all_rented_van = RentedVan.objects.filter(is_done = True).all().order_by('date_recorded')
    return all_rented_van


@register.simple_tag
def get_all_carpooled():
    all_rented_van = CarpoolVan.objects.filter(is_done = True).all().order_by('date_recorded')

    return all_rented_van

@register.simple_tag
def get_rating():

    rating = 10
    whole_number, decimal_part = divmod(rating, 1)

    array = [digit for digit in range(int(whole_number))]
    
    return array, decimal_part





        