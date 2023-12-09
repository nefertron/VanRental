from django import template
from ..models import *
from django.db.models import Q
from django.db.models import Sum
from django.http import JsonResponse


from datetime import datetime, timedelta


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
def get_all_new_gallery(user):
    tour_galleries = TourGallery.objects.filter(tour_category = None, is_enabled = False, rented_van__driver_id__user_id = user).all().order_by('id')
    return tour_galleries


@register.simple_tag
def get_all_new_pending_gallery(user):
    tour_galleries = TourGallery.objects.filter(is_enabled = False, rented_van__driver_id__user_id = user).all().order_by('id')
    return tour_galleries

@register.simple_tag
def get_all_tour_categories():
    tour_categories = TourCategories.objects.filter().all()
    return tour_categories


@register.simple_tag
def get_all_pending_new_gallery(user):
    pending_tour_galleries = TourGallery.objects.filter(is_enabled = False, is_modified = True).all().order_by('id')
    return pending_tour_galleries


@register.simple_tag
def get_all_pending_gallery_images(tour_gallery):
    all_images = TourGalleryImages.objects.filter(tour_gallery = tour_gallery, is_enabled = True).all()

    return all_images


@register.simple_tag
def get_all_pending_gallery_indices(tour_gallery):
    all_images = TourGalleryImages.objects.filter(tour_gallery = tour_gallery, is_enabled = True).count()
    indexes = []

    for i in range(0, all_images):
        indexes.append(i)

    return indexes


@register.simple_tag
def get_all_approved_gallery():
    all_approved_gallery = TourGallery.objects.filter(is_enabled = True).all().order_by('id')
    return all_approved_gallery

@register.simple_tag
def get_all_approved_gallery_indices(tour_gallery):
    all_images = TourGalleryImages.objects.filter(tour_gallery = tour_gallery, is_enabled = True).count()
    indexes = []

    for i in range(0, all_images):
        indexes.append(i)

    return indexes

@register.simple_tag
def get_all_approved_gallery_images(tour_gallery):
    all_images = TourGalleryImages.objects.filter(tour_gallery = tour_gallery, is_enabled = True).all()
    return all_images


@register.simple_tag
def get_all_heart_reactions_count(user, tour_gallery):

    heart_details_storage = None

    all_heart_reactions = HeartReactions.objects.filter(tour = tour_gallery, is_hearted = True).count()

    if not user == 'None':
        heart_checker = HeartReactions.objects.filter(tour = tour_gallery, is_hearted = True, hearted_by = user).first()

        if heart_checker:
            if all_heart_reactions == 2:
                heart_details_storage = f'You and {all_heart_reactions - 1} other'
            elif all_heart_reactions > 2:
                heart_details_storage = f'You and {all_heart_reactions - 1} others'
            else:
                heart_details_storage = f'You'
        else:
            heart_details_storage = all_heart_reactions
    
    else:
        heart_details_storage = all_heart_reactions

    return heart_details_storage


@register.simple_tag
def get_all_tour_comments(tour_gallery):
    
    all_tour_comments = TourCommentSection.objects.filter(tour = tour_gallery).all().order_by('id')

    return all_tour_comments





@register.simple_tag
def van_availability_checker(van):
    date_today = datetime.now().strftime('%Y-%m-%d')

    if RentedVan.objects.filter(plate_no = van, travel_date = date_today).first():
        return False
    else:
        return True

    

    

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
def get_all_messages(user):
    if user:
        all_users = User.objects.filter(~Q(id=user.id)).all()
        last_messages = []

        for acc in all_users:
            # Get the last message sent by acc to the user
            last_msg = Messages.objects.filter(Q(receiver=user, sender=acc) | Q(receiver=acc, sender=user)).last()

            # print(last_msg)
            if last_msg:
                last_messages.append(last_msg)

        # Sort the last_messages list based on the date_sent in descending order
        last_messages.sort(key=lambda x: x.date_sent, reverse=True)

        return last_messages


@register.simple_tag
def get_unseen_messages(user):
    if user:
        all_received_messages = Messages.objects.filter(receiver=user, is_seen = False).count()
        return all_received_messages
    

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
def get_rented_van_image(van):
    van_image = VanImages.objects.filter(van_image_id = van).first()

    if van_image:
        return van_image.vehicle_image
    else:
        return ''

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
def get_available_drivers(excempted_id, date_start, date_end):

    temp_driver_storage = []
    
    all_driver_accounts = DriverAccount.objects.filter(is_verified = True).all()
    for driver in all_driver_accounts:
        all_pending_rental_records = RentedVan.objects.filter(~Q(id = excempted_id),
                                                              is_rejected = False,
                                                              is_cancelled = False,
                                                              is_done = False,
                                                              driver_id = driver).all()
        
        temp_date_storage = []
        for rental_record in all_pending_rental_records:
            rental_start_date = rental_record.travel_date.date()

            while rental_start_date <= (rental_record.travel_date_end.date() if rental_record.travel_date_end else rental_record.travel_date.date()):
                # Format the date as "YYYY-MM-DD" string and append to the list
                formatted_date = rental_start_date.strftime('%Y-%m-%d')
                temp_date_storage.append(formatted_date)
                
                # Move to the next day
                rental_start_date += timedelta(days=1)


        
        travel_date_start = date_start.date()
        driver_is_available = True
        
        while travel_date_start <= (date_end.date() if date_end else travel_date_start):
            # Format the date as "YYYY-MM-DD" string and append to the list
            formatted_travel_date = travel_date_start.strftime('%Y-%m-%d')
            
            if formatted_travel_date in temp_date_storage:
                driver_is_available = False
            
            # Move to the next day
            travel_date_start += timedelta(days=1)


        if driver_is_available:
            temp_driver_storage.append(driver)

    return temp_driver_storage 

@register.simple_tag
def mark_as_done_availability_checker(date_start, date_end):
    travel_date_start = date_start.date()

    temp_date_storage = []

    while travel_date_start <= (date_end.date() if date_end else travel_date_start):
        # Format the date as "YYYY-MM-DD" string and append to the list
        formatted_travel_date = travel_date_start.strftime('%Y-%m-%d')
        temp_date_storage.append(formatted_travel_date)
        
        # Move to the next day
        travel_date_start += timedelta(days=1)

    today_date = datetime.now().date()

    # print(temp_date_storage)
    # print(today_date.strftime('%Y-%m-%d'))
    # print((date_start.date() - today_date).days)
    # print(today_date.strftime('%Y-%m-%d') in temp_date_storage)
    
    days_left = (date_start.date() - today_date).days

    if today_date.strftime('%Y-%m-%d') in temp_date_storage:
        return 'mark_as_done'
    elif days_left < 1:
        return 'mark_as_done'
    else:
        if days_left > 1:
            return f'{days_left} days'
        else:
            return f'{days_left} day'
    

    



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
                                                           is_cancelled = False,
                                                           is_dropped = False).aggregate(all_pending_booked_passengers = Sum('seats_occupied'))['all_pending_booked_passengers']
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
                                                passenger_id = passenger_account).all().order_by('-id')
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



@register.simple_tag
def get_all_FAQs():
    all_faqs = FAQs.objects.filter(is_active = True).all().order_by('id')

    return all_faqs

@register.simple_tag
def get_getInTouch():
    get_in_touch_checker = GetInTouch.objects.filter().first()

    return get_in_touch_checker



@register.simple_tag
def get_color_coding(van):
    if (van.color_coding):
        all_color_coding = van.color_coding.split('|||')
        return all_color_coding
    else:
        return ''
    


@register.simple_tag
def get_all_years():
    today = datetime.now()

    all_years = []

    year_today = today.year

    while year_today != 2019:
        all_years.append(year_today)
        year_today -= 1

    return all_years