from django import template
from ..models import *
from django.db.models import Q
from django.db.models import Sum
from json import dumps
import json

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
def get_unavailable_dates():
    rented_van = RentedVan.objects.all()

    temp_storage = []
    for van in rented_van:
        # Format the date as "YYYY-MM-DD" string and append to the list
        formatted_date = van.travel_date.strftime('%Y-%m-%d')
        temp_storage.append(formatted_date)

    # Convert the list to a JSON string
    return json.dumps(temp_storage)



@register.simple_tag
def get_income_last_month():
    date_today = datetime.now()
    month = date_today.month
    year = date_today.year

    target_month = 0
    target_year = 0
    

    if month == 1:
        target_year = year - 1
        target_month = 12
    else:
        target_year = year
        target_month = month - 1

        if target_month < 10:
            target_month = f'0{target_month}'
        else:
            target_month = target_month
    
    overall_income = 0

    for rent in RentedVan.objects.filter(is_done = True, travel_date__year = target_year, travel_date__month = target_month).all():
        overall_income = overall_income + rent.package_price

    for booked_carpool in BookedPassenger.objects.filter(is_dropped = True, date_dropped__year = target_year, date_dropped__month = target_month ).all():
        overall_income = overall_income + booked_carpool.fare
    
    return overall_income

@register.simple_tag
def get_income_this_month():
    date_today = datetime.now()
    month = date_today.month
    year = date_today.year

    target_month = 0
    if month < 10:
        target_month = f'0{month}'
    else:
        target_month = month

    overall_income = 0

    for rent in RentedVan.objects.filter(is_done = True, travel_date__year = year, travel_date__month = target_month).all():
        overall_income = overall_income + rent.package_price

    for booked_carpool in BookedPassenger.objects.filter(is_dropped = True, date_dropped__year = year, date_dropped__month = target_month).all():
        overall_income = overall_income + booked_carpool.fare

    return overall_income

@register.simple_tag
def get_my_total_availed_services_last_month(passenger_account):
    date_today = datetime.now()
    month = date_today.month
    year = date_today.year

    target_month = 0
    target_year = 0
    

    if month == 1:
        target_year = year - 1
        target_month = 12
    else:
        target_year = year
        target_month = month - 1

        if target_month < 10:
            target_month = f'0{target_month}'
        else:
            target_month = target_month

    all_rental = RentedVan.objects.filter(rented_by = passenger_account, is_done = True, travel_date__year = target_year, travel_date__month = target_month).count()
    all_carpooling = BookedPassenger.objects.filter(passenger_id = passenger_account, is_dropped = True, date_dropped__year = target_year, date_dropped__month = target_month).count()
    total = all_rental + all_carpooling
    return total


@register.simple_tag
def get_my_total_availed_services_this_month(passenger_account):
    date_today = datetime.now()
    month = date_today.month
    year = date_today.year
    
    all_rental = RentedVan.objects.filter(rented_by = passenger_account, is_done = True, travel_date__year = year, travel_date__month = month).count()
    all_carpooling = BookedPassenger.objects.filter(passenger_id = passenger_account, is_dropped = True, date_dropped__year = year, date_dropped__month = month).count()
    total = all_rental + all_carpooling
    return total


@register.simple_tag
def get_my_number_of_travel_last_month(driver_account):
    date_today = datetime.now()
    month = date_today.month
    year = date_today.year

    target_month = 0
    target_year = 0
    

    if month == 1:
        target_year = year - 1
        target_month = 12
    else:
        target_year = year
        target_month = month - 1

        if target_month < 10:
            target_month = f'0{target_month}'
        else:
            target_month = target_month


    all_rental = RentedVan.objects.filter(driver_id = driver_account, is_done = True, travel_date__year = target_year, travel_date__month = target_month).count()
    all_carpooling = CarpoolVan.objects.filter(driver_id = driver_account, is_done = True, date_recorded__year = target_year, date_recorded__month = target_month).count()
    total = all_rental + all_carpooling
    return total


@register.simple_tag
def get_my_number_of_travel_this_month(driver_account):
    date_today = datetime.now()
    month = date_today.month
    year = date_today.year
    
    all_rental = RentedVan.objects.filter(driver_id = driver_account, is_done = True, travel_date__year = year, travel_date__month = month).count()
    all_carpooling = CarpoolVan.objects.filter(driver_id = driver_account, is_done = True, date_recorded__year = year, date_recorded__month = month).count()
    total = all_rental + all_carpooling
    return total


@register.simple_tag
def get_all_rental_services():
    all_rental_services = RentedVan.objects.filter(is_done = True).all()
    return all_rental_services

@register.simple_tag
def get_all_carpool_services():
    all_booked_carpool = BookedPassenger.objects.filter(is_dropped = True).all()
    return all_booked_carpool


@register.simple_tag
def get_my_notifications(user):
    if user:
        my_notifications = Notification.objects.filter(receiver_id = user).all().order_by('-date_recorded')
        return my_notifications
    
@register.simple_tag
def get_unseen_notifications(user):
    if user:
        my_notifications = Notification.objects.filter(receiver_id = user, is_seen = False).count()
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
    all_to_carpool_vans = CarpoolVan.objects.filter(is_done = False).all()

    return all_to_carpool_vans



@register.simple_tag
def get_available_seats_in_carpool(van):
    return 0

@register.simple_tag
def get_all_passengers_in_carpool(carpool):
    get_total_of_bookings = BookedPassenger.objects.filter(carpool_id = carpool).count()
    get_all_seats_occupied_by_passengers = BookedPassenger.objects.filter(carpool_id = carpool).aggregate(get_all_seats_occupied_by_passengers = Sum('seats_occupied'))['get_all_seats_occupied_by_passengers']
    
    if not get_total_of_bookings is None:
        return get_total_of_bookings, get_all_seats_occupied_by_passengers
    else:
        return 0, 0

@register.simple_tag
def get_all_done_rental():
    all_rented_van = RentedVan.objects.filter(is_done = True).all().order_by('-date_recorded')
    return all_rented_van

@register.simple_tag
def get_all_done_carpool():
    all_carpooled_van = CarpoolVan.objects.filter(is_done = True).all().order_by('-date_recorded')
    return all_carpooled_van


@register.simple_tag
def get_all_carpooled():
    all_rented_van = CarpoolVan.objects.filter(is_done = True).all().order_by('-date_recorded')

    return all_rented_van


@register.simple_tag
def get_overall_rental_rating(id):
    get_all_rental_ratings = Review.objects.filter(rent_id = id).aggregate(get_all_rental_ratings = Sum('rating'))['get_all_rental_ratings']
    get_all_rental_reviews_count = Review.objects.filter(rent_id = id).count()

    if get_all_rental_reviews_count > 0:
        rating = (get_all_rental_ratings/get_all_rental_reviews_count)
        whole_number, decimal_part = divmod(rating, 1)

        array = [digit for digit in range(int(whole_number))]
        
        return array, decimal_part
    else:
        return 0,0
    

@register.simple_tag
def get_overall_carpool_rating(carpool_id):
    carpool = CarpoolVan.objects.filter(id=carpool_id).first()

    get_all_rental_ratings = Review.objects.filter(carpool_id__carpool_id = carpool).aggregate(get_all_rental_ratings = Sum('rating'))['get_all_rental_ratings']
    get_all_rental_reviews_count = Review.objects.filter(carpool_id__carpool_id = carpool).count()

    if get_all_rental_reviews_count > 0:
        rating = (get_all_rental_ratings/get_all_rental_reviews_count)
        whole_number, decimal_part = divmod(rating, 1)

        array = [digit for digit in range(int(whole_number))]
        
        return array, decimal_part
    else:
        return 0,0


@register.simple_tag
def get_rental_reviews(id):
    all_reviews = Review.objects.filter(rent_id = id).all().order_by('-date_recorded')
    return all_reviews

@register.simple_tag
def get_carpool_reviews(carpool_id):
    all_reviews = Review.objects.filter(carpool_id__carpool_id = carpool_id).all().order_by('-date_recorded')
    return all_reviews

@register.simple_tag
def check_if_part_of_carpooling(carpool, passenger_account):
    booking = BookedPassenger.objects.filter(carpool_id = carpool, passenger_id = passenger_account).first()

    if booking:
        return True
    else:
        return False
    

@register.simple_tag
def convert_rating_to_array(num):
    array = []

    for i in range(0, num):
        array.append(i)

    return array

@register.simple_tag
def get_all_municipality():
    return ListOfMunicipalities.objects.filter().all()


@register.simple_tag
def get_available_drivers():
    all_driver_accounts = DriverAccount.objects.filter(is_available = True, is_verified = True).all()

    return all_driver_accounts 


@register.simple_tag
def get_total_open_bookings():
    total_open_bookings = RentedVan.objects.filter(is_done = False, is_rejected = False, is_confirmed = False, is_cancelled = False).count()

    return total_open_bookings

@register.simple_tag
def get_total_open_carpool():
    total_open_carpool = CarpoolVan.objects.filter(is_done = False).count()
    return total_open_carpool

@register.simple_tag
def get_available_number_of_seats_in_carpooling(carpool):
    all_booked_passengers = BookedPassenger.objects.filter(carpool_id = carpool,
                                                           is_confirmed = True,
                                                           is_dropped = False).aggregate(all_booked_passengers = Sum('seats_occupied'))['all_booked_passengers']
    
    if not all_booked_passengers is None:
        remaining_available_seats = carpool.available_seat - all_booked_passengers
        return remaining_available_seats
    else:
        return carpool.available_seat
    
@register.simple_tag
def get_pending_number_of_seats_in_carpooling(carpool):
    all_pending_booked_passengers = BookedPassenger.objects.filter(carpool_id = carpool,
                                                           is_confirmed = False,
                                                           is_rejected = False,
                                                           is_cancelled = False,).aggregate(all_pending_booked_passengers = Sum('seats_occupied'))['all_pending_booked_passengers']
    if not all_pending_booked_passengers is None:
        return all_pending_booked_passengers
    else:
        return 0
    

@register.simple_tag
def get_all_pending_booked_passengers_in_carpooling(carpool):

    all_booked_passengers = BookedPassenger.objects.filter(carpool_id = carpool,
                                                           is_confirmed = False,
                                                           is_rejected = False,
                                                           is_cancelled = False,
                                                           is_dropped = False).all()
    return all_booked_passengers


@register.simple_tag
def get_all_confirmed_booked_passengers_in_carpooling(carpool):
    all_booked_passengers = BookedPassenger.objects.filter(carpool_id = carpool,
                                                           is_confirmed = True,
                                                           is_rejected = False,
                                                           is_cancelled = False,
                                                           is_dropped = False).all()
    return all_booked_passengers

@register.simple_tag
def get_all_dropped_booked_passengers_in_carpooling(carpool):
    all_booked_passengers = BookedPassenger.objects.filter(carpool_id = carpool,
                                                           is_dropped = True).all()
    return all_booked_passengers


@register.simple_tag
def get_my_carpool_booking_information(carpool, passenger_account):
    my_carpool_booking_information = []

    my_carpools = BookedPassenger.objects.filter(carpool_id = carpool,
                                                passenger_id = passenger_account).all()
    if my_carpools:
        for carpool in my_carpools:
            dictionary = {}
            if carpool.is_confirmed:
                dictionary['Status'] = 'Confirmed'
            elif carpool.is_rejected:
                dictionary['Status'] = 'Rejected'
            elif carpool.is_cancelled:
                dictionary['Status'] = 'Cancelled'
            elif carpool.is_dropped:
                dictionary['Status'] = 'Dropped'
            else:
                dictionary['Status'] = 'Pending'

            dictionary['BookID'] = carpool.booked_id
            dictionary['SeatsOccupied'] = carpool.seats_occupied
            dictionary['PickUpLocation'] = carpool.pick_up_location
            dictionary['Destination'] = carpool.destination
            dictionary['Fare'] = carpool.fare
            dictionary['MyBookedID'] = carpool.id

            my_carpool_booking_information.append(dictionary)

        return my_carpool_booking_information
    else:
        return None

@register.simple_tag
def get_total_pending_bookings(user):
    
    driver_account = DriverAccount.objects.filter(user_id = user).first()
    passenger_account = PassengerAccount.objects.filter(user_id = user).first()

    if not driver_account is None:
        total_open_bookings = RentedVan.objects.filter(is_rejected = False, is_confirmed = False, is_done = False, is_cancelled = False).count()
        return total_open_bookings
    else:
        total_open_bookings = RentedVan.objects.filter(rented_by = passenger_account, is_rejected = False, is_confirmed = False, is_done = False, is_cancelled = False).count()
        return total_open_bookings


@register.simple_tag
def get_total_confirmed_bookings():
    total_confirmed_bookings = RentedVan.objects.filter(is_done = False, is_rejected = False, is_confirmed = True).count()

    return total_confirmed_bookings


@register.simple_tag
def get_total_pending_drivers():
    total_pending_drivers = DriverAccount.objects.filter(is_verified = False, auth_token = None).count()

    return total_pending_drivers





        