from django.shortcuts import render, redirect

from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from datetime import datetime, timedelta
import uuid

from django.conf import settings
from django.core.mail import send_mail

from django.http import JsonResponse
from json import dumps
import json
from django.core.serializers import serialize
from django.utils import timezone


from django.db import transaction
from django.db.models import Sum, Q

# Create your views here.

################ REUSABLE REMOVE SPACES DEF FUNCTION
def RemoveSpaces(name):
    li = list(name.split(" "))
    temp_container = ''.join(li)

    return temp_container

################ REUSABLE CREATE NOTIFICATION DEF FUNCTION
def create_notification(request, user_id, message):
    create_notif = Notification.objects.create(receiver_id = user_id,
                                                        message = message,
                                                        date_recorded = datetime.now())
    create_notif.notification_id = f'NOTF{create_notif.id}'
    create_notif.save()


################ REUSABLE LOG IN DEF FUNCTION
def loginAccount(request, username, password):
    username = RemoveSpaces(username.lower())
    if '@' in username:
        user = User.objects.filter(email = username).first()

        if user:
            to_login = authenticate(username = user.username, password = password)
            
            if to_login is None:
                messages.info(request, 'Sorry, the password you entered is invalid. Please try again!')
                return 'invalid'
            else:
                passenger_account = PassengerAccount.objects.filter(user_id = user, is_verified = True).first()
                admin_account = AdminAccount.objects.filter(user_id = user, is_verified = True).first()
                driver_account = DriverAccount.objects.filter(user_id = user, is_verified = True).first()
                if passenger_account or admin_account or driver_account:
                    login(request, user)
                    messages.info(request, 'You logged in successfully!')
                    if passenger_account:
                        return 'passenger'
                    else:
                        return 'not_passenger'
                else:
                    if passenger_account:
                        messages.info(request, 'It seems like your account is not verified yet. Please check your email for the verification')
                    else:
                        messages.info(request, 'It seems like your account is not verified yet. Please contact the administrator to verify your account!')
                    return 'invalid'
        else:
            messages.info(request, f'Sorry, we couldn`t find an account with email {username}!')
            return 'invalid'

    else:
        user = User.objects.filter(username = username).first()
        if user:
            to_login = authenticate(username = username, password = password)
            if to_login is None:
                messages.info(request, 'Sorry, the password you entered is invalid. Please try again!')
                return 'invalid'
            else:
                passenger_account = PassengerAccount.objects.filter(user_id = user, is_verified = True).first()
                admin_account = AdminAccount.objects.filter(user_id = user, is_verified = True).first()
                driver_account = DriverAccount.objects.filter(user_id = user, is_verified = True).first()
                if passenger_account or admin_account or driver_account:
                    login(request, user)
                    messages.info(request, 'You logged in successfully!')

                    if passenger_account:
                        return 'passenger'
                    else:
                        return 'not_passenger'
                else:
                    if passenger_account:
                        messages.info(request, 'It seems like your account is not verified yet. Please check your email for the verification')
                    else:
                        messages.info(request, 'It seems like your account is not verified yet. Please contact the administrator to verify your account!')
                    return 'invalid'
        else:
            messages.info(request, f'Sorry, we couldn`t find an account with username {username}!')
            return 'invalid'

################ REUSABLE BOOKING DEF FUNCTION


################ TRAVEL DATE CONVERTER
def convertTravelDateFrom(date, time):
    travel_date_start = datetime.strptime(date, '%Y-%m-%d')
    start_time = datetime.strptime(time, '%I:%M %p').time()

    complete_travel_date_start = datetime.combine(travel_date_start, start_time)

    return complete_travel_date_start


def convertTravelDateTo(date, time):
    travel_date_end = datetime.strptime(date, '%Y-%m-%d')
    end_time = datetime.strptime(time, '%I:%M %p').time()
    
    complete_travel_date_end = datetime.combine(travel_date_end, end_time)

    return complete_travel_date_end
################ TRAVEL DATE CONVERTER



################ HOME PAGE
def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        van_id = request.POST.get('van_id')
        from_destination_municipality_id = request.POST.get('from_destination_municipality')
        from_destination = request.POST.get('from_destination')
        to_destination_municipality_id = request.POST.get('to_destination_municipality')
        to_destination = request.POST.get('to_destination')

        travel_start_date = request.POST.get('travel_date_start')
        time_start = request.POST.get('time_start')
        
        travel_end_date = request.POST.get('travel_date_end')
        time_end = request.POST.get('time_end')

        pick_up_location  = request.POST.get('pick_up_location')



        if username and password:
            log_in_attempt = loginAccount(request, username, password)

            if log_in_attempt == 'invalid':
                return redirect('/login')
            elif log_in_attempt == 'passenger':
                return redirect('/index')
            else:
                return redirect('/dashboard')
        
        else:
            _from_municipality = ListOfMunicipalities.objects.filter(id = from_destination_municipality_id).first()
            _to_municipality = ListOfMunicipalities.objects.filter(id = to_destination_municipality_id).first()

            travel_date_from = convertTravelDateFrom(travel_start_date, time_start)
            travel_date_to = convertTravelDateTo(travel_end_date, time_end)

            create_rent_van = RentedVan.objects.create(plate_no = Van.objects.filter(id = van_id).first(),
                                                        rented_by = request.user.passengeraccount,
                                                        from_destination = f'{from_destination}, {_from_municipality.municipality_name}',
                                                        to_destination = f'{to_destination}, {_to_municipality.municipality_name}',
                                                        travel_date = travel_date_from,
                                                        travel_date_end = travel_date_to,
                                                        pick_up_location = pick_up_location,
                                                        date_recorded = datetime.now())
            create_rent_van.rent_id = f'RENT{create_rent_van.id}'
            create_rent_van.save()

            message = f'You successfully set a booking. Please wait for the confirmation of the admin. Please note that the rent will be set later by the admin after. You can either set an offer or accept the set price.'
            create_notification(request, request.user, message)

            admin_account = User.objects.filter(is_superuser = True).first()
            message_to_admin = f'{request.user.first_name} {request.user.last_name} set a booking with a scheduled date {travel_date_from}. Please visit the booking section for more details.'
            create_notification(request, admin_account, message_to_admin)

            messages.info(request, message)

            return redirect('/pending-booking')


    return render(request, 'homepage/index.html')

################ DASHBOARD PAGE
def dashboard(request):
    if not request.user.is_authenticated:
        messages.info(request, 'The page you are trying to access is not available because you are already logged in!')
        return redirect('/login')

    return render(request, 'homepage/dashboard.html')
    


################ LOGIN PAGE
def login_page(request):
    if request.user.is_authenticated:
        messages.info(request, 'The page you are trying to access is not available because you are already logged in!')
        return redirect('/index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        log_in_attempt = loginAccount(request, username, password)

        if log_in_attempt == 'invalid':
            return redirect('/login')
        elif log_in_attempt == 'passenger':
            return redirect('/index')
        else:
            return redirect('/dashboard')
    
    return render(request, 'authentication/login.html')



################ SIGNUP PAGE
def signup_page(request):
    if request.user.is_authenticated:
        messages.info(request, 'The page you are trying to access is not available because you are already logged in!')
        return redirect('/index')


    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        bday = request.POST.get('bday')
        contact_no = request.POST.get('contact_no')
        address = request.POST.get('address')
        pass1 = request.POST.get('pass1')
        driverOrPassenger = request.POST.get('user_type')

        context = {
            'username' : username, 
            'fname' : fname,
            'lname' : lname,
            'email' : email,
            'bday' : bday,
            'contact_no' : contact_no,
            'address' : address,
            'driverOrPassenger' : driverOrPassenger
        }

        

        if User.objects.filter(username = username).first():
            messages.info(request, f'The username you entered is unavailable. Please try another!')
            return render(request, 'authentication/signup.html', context)
        elif User.objects.filter(email = email).first():
            return render(request, 'authentication/signup.html', context)

        else:
            username = RemoveSpaces(username.lower())

            email = RemoveSpaces(email.lower())
        
            if driverOrPassenger == 'passenger':
                new_user = User.objects.create(email = email, username = username, first_name = fname, last_name = lname)
                new_user.set_password(pass1)
                new_user.save()
                
                auth_token = str(uuid.uuid4())

                new_passenger = PassengerAccount.objects.create(
                    user_id = new_user,
                    bday = bday,
                    contact_no = contact_no,
                    address = address,
                    auth_token = auth_token)
                
                new_passenger.passenger_id = f'PASS{new_passenger.id}'
                new_passenger.save()

                host = request.get_host()
                send_registration_email(new_user, 'passenger', auth_token, host)
                
                message = 'Your account has been successfully created.'
                create_notification(request, new_user, message)

                messages.info(request, f'Your account has been successfully created. Please check your email to verify your account!')
                return redirect('/login')

            else:
                new_user = User.objects.create(email = email, username = username, first_name = fname, last_name = lname)
                new_user.set_password(pass1)
                new_user.save()

                new_driver = DriverAccount.objects.create(
                    user_id = new_user,
                    bday = bday,
                    contact_no = contact_no,
                    address = address)
                
                new_driver.driver_id = f'DRVR{new_driver.id}'
                new_driver.save()

                messages.info(request, f'Your account has been successfully created. Please contact the administrator to send you an email to confirm your account!')
                return redirect('/login')


    return render(request, 'authentication/signup.html')


################ EMAIL GENERATOR
def send_registration_email(account, account_type, auth_token, host):
    subject = 'Welcome to VAN RENTAL online portal!'
    message = f'Thank you for signing up on our page.\nPlease click the link below to complete the account activation process.\nhttp://{host}/verify/{account_type}/{auth_token}'
    from_mail = settings.EMAIL_HOST_USER
    recipient_list = [account.email]

    send_mail(subject, message, from_mail, recipient_list)


################ ACCOUNT VERIFICATION
def verify(request, account_type, auth_token):
    if account_type == 'passenger':
        pending_passenger = PassengerAccount.objects.filter(auth_token = auth_token).first()
        if pending_passenger:
            pending_passenger.is_verified = True
            pending_passenger.auth_token = None
            pending_passenger.save()

            messages.info(request, 'Your account has been verified successfully! Please login your account')

            message = f'Hello {pending_passenger.user_id.first_name}! Thank you for signing on our page! Enjoy renting!'
            create_notification(request, pending_passenger.user_id, message)
            
            return redirect('/login')
        else:
            messages.info(request, f'Sorry, the page you are trying to access is invalid or expired. Please try another!')
            return redirect('/login')
        
    else:
        pending_driver = DriverAccount.objects.filter(auth_token = auth_token).first()
        if pending_driver:
            pending_driver.is_verified = True
            pending_driver.auth_token = None
            pending_driver.save()

            messages.info(request, 'Your account has been verified successfully! Please login your account')

            message = f'Hello {pending_driver.user_id.first_name}! Thank you for signing on our page! Happy driving!'
            create_notification(request, pending_driver.user_id, message)

            return redirect('/login')
        else:
            messages.info(request, f'Sorry, the page you are trying to access is invalid or expired. Please try another!')
            return redirect('/login')




################ PROFILE PAGE
def profile(request):
    if not request.user.is_authenticated:
        messages.info(request, 'The page you are trying to access is not available. Please login first!')
        return redirect('/login')


    admin_account = AdminAccount.objects.filter(user_id = request.user).first()
    driver_account = DriverAccount.objects.filter(user_id = request.user).first()
    passenger_account = PassengerAccount.objects.filter(user_id = request.user).first()

    context = {}

    if not admin_account is None:
        context['profile'] = admin_account
        context['account_type'] = 'Admin Account'
        context['account_id'] = f'ADM{admin_account.id}'

    elif not driver_account is None:
        context['profile'] = driver_account
        context['account_type'] = 'Driver Account'
        context['account_id'] = driver_account.driver_id

    elif not passenger_account is None:
        context['profile'] = passenger_account
        context['account_type'] = 'Passenger Account'
        context['account_id'] = passenger_account.passenger_id


    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        bday = request.POST.get('bday')
        contact_no = request.POST.get('contact_no')
        address = request.POST.get('address')

        new_profile  = request.POST.get('new_profile')
        remove_profile = request.POST.get('remove_profile')

        if new_profile:
            if len(new_profile) > 0:
                context['profile'].profile = new_profile
                context['profile'].save()
                messages.info(request, f'Your profile has been saved!')
                return redirect('/profile')

        if remove_profile:
            if remove_profile == "True":
                context['profile'].profile = None
                context['profile'].save()
                messages.info(request, f'Your profile has been removed!')
                return redirect('/profile')
        
        if User.objects.filter(email = email).count() > 1:
            messages.info(request, f'Sorry, the email you entered is not available. Please try another!')
            return redirect('/profile')
        

        else:
            email = RemoveSpaces(email.lower())

            all_changes = []
            
            if fname != context["profile"].user_id.first_name:
                all_changes.append('first name')

            if lname != context["profile"].user_id.last_name:
                all_changes.append('last name')

            if email != context["profile"].user_id.email:
                all_changes.append('email')
            
            if bday != context["profile"].bday:
                all_changes.append('birth date')
            
            if contact_no != context["profile"].contact_no:
                all_changes.append('contact no.')

            if address != context["profile"].address:
                all_changes.append('address')

            User.objects.filter(id = request.user.id).update(first_name = fname,
                                        last_name = lname,
                                        email = email)

            context['profile'].bday = bday
            context['profile'].contact_no = contact_no
            context['profile'].address = address
            context['profile'].save()


            list_of_changes = ", ".join(all_changes)

            if len(all_changes) > 1:
                message = f"The changes in fields {list_of_changes} have been saved."
                messages.info(request, message)
            elif len(all_changes) == 1 and all_changes[0] != 'birth date':
                message = f"The change in your {list_of_changes} has been saved."
                messages.info(request, message)
            else:
                messages.info(request, 'It seems like you made no changes')

            return redirect('/profile')

    return render(request, 'profile/profile.html', context)


################ RENT A VAN PAGE
def rent_van(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Please login to continue')
        return redirect('/login')
    
    if request.user.is_superuser:
        messages.info(request, 'The page you are trying to access is not available.')
        return redirect('/index')
    

    all_vans = Van.objects.filter().all()
    
    context = {
        'all_vans' : all_vans
    }


    if request.method == 'POST':
        package_rent = request.POST.get('package_rent')
        van_id = request.POST.get('van_id')
        from_destination_municipality_id = request.POST.get('from_destination_municipality')
        from_destination = request.POST.get('from_destination')
        to_destination_municipality_id = request.POST.get('to_destination_municipality')
        to_destination = request.POST.get('to_destination')
        travel_date = request.POST.get('travel_date')


        _from_municipality = ListOfMunicipalities.objects.filter(id = from_destination_municipality_id).first()
        _to_municipality = ListOfMunicipalities.objects.filter(id = to_destination_municipality_id).first()

        create_rent_van = RentedVan.objects.create(plate_no = Van.objects.filter(id = van_id).first(),
                                                    rented_by = request.user.passengeraccount,
                                                    package_price = package_rent,
                                                    from_destination = f'{from_destination}, {_from_municipality.municipality_name}',
                                                    to_destination = f'{to_destination}, {_to_municipality.municipality_name}',
                                                    travel_date = travel_date,
                                                    date_recorded = datetime.now())
        create_rent_van.rent_id = f'RENT{create_rent_van.id}'
        create_rent_van.save()

        message = f'You successfully set a booking. Please wait for the confirmation of the admin. Please note that the rent is subjected to an adjustment.'
        create_notification(request, request.user, message)

        admin_account = User.objects.filter(is_superuser = True).first()
        message_to_admin = f'{request.user.first_name} {request.user.last_name} set a booking with a scheduled date {travel_date}. Please visit the booking section for more details.'
        create_notification(request, admin_account, message_to_admin)

        messages.info(request, message)
        return redirect('/pending-booking')





    return render(request, 'vans/rent-a-van.html', context)
    




################ PENDING DRIVERS PAGE
def pending_drivers(request):
    if not request.user.is_superuser:
        messages.info(request, 'The page you are trying to access is not available.')
        return redirect('/index')
    
    all_pending_drivers = DriverAccount.objects.filter(is_verified = False, auth_token = None).all()

    context = {
        'all_pending_drivers' : all_pending_drivers
    }


    if request.method == 'POST':
        send_email_to_this_id = request.POST.get('send_email_to_this_id')

        driver_account = DriverAccount.objects.filter(id = send_email_to_this_id).first()

        if driver_account:
            auth_token = str(uuid.uuid4())
            driver_account.auth_token = auth_token
            driver_account.save()

            host = request.get_host()
            send_registration_email(driver_account.user_id, 'driver', auth_token, host)

            message = f'An email verification is sent to {driver_account.user_id.first_name} {driver_account.user_id.last_name} with email {driver_account.user_id.email}. If you want to contact him, use this number ({driver_account.contact_no})'
            create_notification(request, request.user, message)
            messages.info(request, message)
            return redirect('/pending-drivers')
        
        else:
            messages.info(request, f'Sorry, something went wrong. Please try again!')
            return redirect('/pending-drivers')

    return render(request, 'pending/pending-drivers.html', context)


def list_of_vans(request):
    if not request.user.is_authenticated:
        messages.info(request, 'The page you are trying to access is not available. Please login first!')
        return redirect('/login')

    context = {
        'all_vans' : Van.objects.filter().all()
    }

    if request.method == "POST":
        images = request.POST.get('images')
        plate_no = request.POST.get('plate_no')
        color = request.POST.get('color')
        number_of_seats = request.POST.get('number_of_seats')
        description = request.POST.get('description')
        brand_name = request.POST.get('brand_name')
        is_airconditioned = request.POST.get('is_airconditioned')

        image_list = images.split('|||') # use to split the image addresses generated by the javascript
        plate_no = RemoveSpaces(plate_no)

        if Van.objects.filter(plate_no = plate_no).first():
            messages.info(request, f'It seems like the Plate No. you entered is already existing, perhaps you made a mistake?')
            return redirect('/list-of-vans')
        
        else:
            if len(image_list) > 0:
                trueOrFalse = True
                if is_airconditioned == 'yes':
                    trueOrFalse = True
                else:
                    trueOrFalse = False
                    
                new_van = Van.objects.create(plate_no = plate_no, 
                                             color = color, 
                                             number_of_seats = number_of_seats, 
                                             description = description,
                                             brand_name = brand_name,
                                             is_airconditioned = trueOrFalse)
                new_van.save()

                for image_src in image_list:
                    attached_image = VanImages.objects.create(van_image_id = new_van, vehicle_image = image_src)
                    attached_image.save()

                message = f'You saved new van information with Plate No. {plate_no}, and attached a total of {len(image_list)} image/s.'
                messages.info(request, message)
                create_notification(request, request.user, message)
                return redirect('/list-of-vans')

            else:
                messages.info(request, f'You must attach atleast 1 image of your van. Please try again!')
                return redirect('/list-of-vans')

    return render(request, 'vans/list-of-vans.html', context)

################ RENT BOOKING LIST PAGE
def rent_booking_list(request):
    if not request.user.is_superuser:
        messages.info(request, 'The page you are trying to access is not available')
        return redirect('/index')

    all_pending_bookings = RentedVan.objects.filter(is_done=False, is_rejected=False, is_cancelled = False, is_confirmed=False).all()

    context = {
        'all_pending_bookings' : all_pending_bookings,
    }

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        driver_id = request.POST.get('driver_id')

        package_rent = request.POST.get('package_rent')

        rejected_booking_id = request.POST.get('rejected_booking_id')

        change_price = request.POST.get('change_price')


        if not driver_id is None:
            booking_target = RentedVan.objects.filter(id = booking_id).first()
            driver_target = DriverAccount.objects.filter(id = driver_id).first()

            booking_target.driver_id = driver_target
            booking_target.is_confirmed = True
            booking_target.save()

            message_to_admin = f'You confirmed a rent booking with RENT ID : {booking_target.rent_id}, with destination FROM {booking_target.from_destination} TO {booking_target.to_destination} on {booking_target.travel_date}'
            message_to_driver = f'You have been assigned as a driver in a rent booking with RENT ID : {booking_target.rent_id}, with destination FROM {booking_target.from_destination} TO {booking_target.to_destination} on {booking_target.travel_date}'
            message_to_passenger = f'Your rent booking with RENT ID : {booking_target.rent_id} has been confirmed, with destination FROM {booking_target.from_destination} TO {booking_target.to_destination} on {booking_target.travel_date}'
            
            driver_target.is_available = False
            driver_target.save()


            create_notification(request, request.user, message_to_admin)
            create_notification(request, driver_target.user_id, message_to_driver)
            create_notification(request, booking_target.rented_by.user_id, message_to_passenger)

            messages.info(request, message_to_admin)
            return redirect('/rent-booking')
        

        elif not rejected_booking_id is None:
            booking_target = RentedVan.objects.filter(id = rejected_booking_id).first()
            booking_target.is_rejected = True
            booking_target.save()

            message_to_admin = f'REJECTED || A rent booking with RENT ID : {booking_target.rent_id}, with destination FROM {booking_target.from_destination} TO {booking_target.to_destination} on {booking_target.travel_date}'
            message_to_passenger = f'REJECTED || Your rent booking with RENT ID : {booking_target.rent_id}, with destination FROM {booking_target.from_destination} TO {booking_target.to_destination} on {booking_target.travel_date}'
            
            create_notification(request, request.user, message_to_admin)
            create_notification(request, booking_target.rented_by.user_id, message_to_passenger)

            messages.info(request, message_to_admin)
            return redirect('/rent-booking')
        
        elif not package_rent is None:
            booking_target = RentedVan.objects.filter(id = booking_id).first()
            booking_target.package_price = package_rent
            booking_target.save()

            message_to_admin = f'You set {package_rent} Php as package rent of booking with RENT ID : {booking_target.rent_id}, with destination FROM {booking_target.from_destination} TO {booking_target.to_destination} on {booking_target.travel_date}'
            message_to_passenger = f'The admin set {package_rent} Php as package rent of your booking with RENT ID : {booking_target.rent_id}, and has a destination FROM {booking_target.from_destination} TO {booking_target.to_destination} on {booking_target.travel_date}. Please view your booking status and choose either accept the price or make an offer.'
            
            create_notification(request, request.user, message_to_admin)
            create_notification(request, booking_target.rented_by.user_id, message_to_passenger)

            messages.info(request, message_to_admin)
            return redirect('/rent-booking')
        
        elif not change_price is None:
            change_price_target = RentedVan.objects.filter(id = booking_id).first()

            message_to_admin = f'You changed the rental for the booking with RENT ID : {change_price_target.rent_id} from {change_price_target.package_price} Php to {change_price} Php.'
            message_to_passenger = f'The admin changed the rental for your booking with RENT ID : {change_price_target.rent_id} from {change_price_target.package_price} Php to {change_price} Php.'
            
            change_price_target.package_price = change_price
            change_price_target.save()

            create_notification(request, request.user, message_to_admin)
            create_notification(request, change_price_target.rented_by.user_id, message_to_passenger)

            messages.info(request, message_to_admin)
            return redirect('/rent-booking')

        
    return render(request, 'vans/rent-booking.html', context)



################ PENDING BOOKING PAGE
def pending_booking(request):
    if not request.user.is_authenticated:
        messages.info(request, f'You must login to continue.')
        return redirect('/login')
    if request.user.is_superuser:
        messages.info(request, f'The page you are trying to access is not available.')
        return redirect('/login')

    driver_account = DriverAccount.objects.filter(user_id = request.user).first()
    passenger_account = PassengerAccount.objects.filter(user_id = request.user).first()

    context = {}

    if not driver_account is None:
        context['profile'] = driver_account
        context['account_type'] = 'Driver'
        context['all_pending_bookings']= RentedVan.objects.filter(is_rejected = False, is_confirmed = False, is_done = False, is_cancelled = False).all().order_by('date_recorded')
    elif not passenger_account is None:
        context['profile'] = passenger_account
        context['account_type'] = 'Passenger'
        context['all_pending_bookings']= RentedVan.objects.filter(rented_by = passenger_account, is_rejected = False, is_confirmed = False, is_done = False, is_cancelled = False).all().order_by('date_recorded')

    if request.method == 'POST':
        cancel_booking_id = request.POST.get('cancel_booking_id')
        
        attached_note = request.POST.get('attached_note')
        set_offer_price = request.POST.get('set_offer_price')
        booking_id_set_offer = request.POST.get('booking_id_set_offer')

        accept_price_booking_id = request.POST.get('accept_price_booking_id')

        if cancel_booking_id:
            to_cancel_rent = RentedVan.objects.filter(id = cancel_booking_id).first()
            to_cancel_rent.is_cancelled = True
            to_cancel_rent.is_confirmed = False
            to_cancel_rent.save()
            
            message_to_passenger = f'CANCELLED || Your rent booking with RENT ID : {to_cancel_rent.rent_id}, with destination FROM {to_cancel_rent.from_destination} TO {to_cancel_rent.to_destination} on {str(to_cancel_rent.travel_date)}'
            
            create_notification(request, to_cancel_rent.rented_by.user_id, message_to_passenger)

            messages.info(request, f'The rent booking with RENT ID : {to_cancel_rent.rent_id} has been cancelled successfully.')
            return redirect('/pending-booking')
        
        elif booking_id_set_offer:

            to_set_offer_booking = RentedVan.objects.filter(id = booking_id_set_offer).first()
            to_set_offer_booking.my_offer = set_offer_price
            to_set_offer_booking.save()

            admin_account = User.objects.filter(is_superuser = True).first()

            create_new_message = Messages.objects.create(sender = request.user,
                                                        receiver = admin_account,
                                                        date_sent = datetime.now(),
                                                        rental_attachment = to_set_offer_booking,
                                                        offer = set_offer_price,
                                                        message = attached_note)
            create_new_message.message_id = f'MSG{create_new_message.id}'
            create_new_message.save()

            message_to_admin = f'OFFER || The user set an offer to a booking with RENT ID : {to_set_offer_booking.rent_id} to {set_offer_price} php.'
            message_to_passenger = f'OFFER || You set {set_offer_price} php as your offer to a booking with RENT ID : {to_set_offer_booking.rent_id}'
            
            create_notification(request, admin_account, message_to_admin)
            create_notification(request, request.user, message_to_passenger)

            messages.info(request, message_to_passenger)
            return redirect('/pending-booking')

        elif accept_price_booking_id:

            accept_booking_price = RentedVan.objects.filter(id = accept_price_booking_id).first()
            accept_booking_price.my_offer = 0
            accept_booking_price.is_accepted = True
            accept_booking_price.save()

            admin_account = User.objects.filter(is_superuser = True).first()

            message_to_admin = f'ACCEPTED || The user accepted the package price of {accept_booking_price.package_price} Php for booking with RENT ID : {accept_booking_price.rent_id}'
            message_to_passenger = f'ACCEPTED || You accepted the package price of {accept_booking_price.package_price} Php for booking with RENT ID : {accept_booking_price.rent_id}'

            create_notification(request, admin_account, message_to_admin)
            create_notification(request, request.user, message_to_passenger)

            messages.info(request, message_to_passenger)
            messages.info(request, 'Please wait for the admin to select a driver for your ride. Thank you!')
            return redirect('/pending-booking')
            


    return render(request, 'vans/pending-booking.html', context)


################ CANCELLED BOOKING PAGE
def cancelled_booking(request):
    context = {}

    passenger_account = PassengerAccount.objects.filter(user_id = request.user).first()

    if not passenger_account is None:
        context['profile'] = passenger_account
        context['all_cancelled_bookings']= RentedVan.objects.filter(rented_by = passenger_account, is_cancelled = True).all().order_by('-date_recorded')
    else:
        context['profile'] = passenger_account
        context['all_cancelled_bookings']= RentedVan.objects.filter(is_cancelled = True).all().order_by('-date_recorded')


    return render(request, 'vans/cancelled-booking.html', context)




################ REJECTED BOOKING PAGE
def rejected_booking(request):
    if not request.user.is_authenticated:
        messages.info(request, f'You must login to continue.')
        return redirect('/login')

    admin_account = AdminAccount.objects.filter(user_id = request.user).first()
    driver_account = DriverAccount.objects.filter(user_id = request.user).first()
    passenger_account = PassengerAccount.objects.filter(user_id = request.user).first()

    context = {}

    if not admin_account is None:
        context['profile'] = admin_account
        context['account_type'] = 'Admin'
        context['all_rejected_bookings'] = RentedVan.objects.filter(is_rejected = True).all().order_by('date_recorded')
    elif not driver_account is None:
        context['profile'] = driver_account
        context['account_type'] = 'Driver'
        context['all_rejected_bookings']= RentedVan.objects.filter(driver_id = driver_account, is_rejected = True).all().order_by('date_recorded')
    elif not passenger_account is None:
        context['profile'] = passenger_account
        context['account_type'] = 'Passenger'
        context['all_rejected_bookings']= RentedVan.objects.filter(rented_by = passenger_account, is_rejected = True).all().order_by('date_recorded')


    return render(request, 'vans/rejected-booking.html', context)




################ CONFIRMED BOOKING PAGE
def confirmed_bookings(request):

    if not request.user.is_authenticated:
        messages.info(request, f'You must login to continue.')
        return redirect('/login')

    admin_account = AdminAccount.objects.filter(user_id = request.user).first()
    driver_account = DriverAccount.objects.filter(user_id = request.user).first()
    passenger_account = PassengerAccount.objects.filter(user_id = request.user).first()

    context = {}

    if not admin_account is None:
        context['profile'] = admin_account
        context['account_type'] = 'Admin'
        context['all_confirmed_bookings'] = RentedVan.objects.filter(is_done=False, is_rejected=False, is_cancelled=False, is_confirmed=True).all()
    elif not driver_account is None:
        context['profile'] = driver_account
        context['account_type'] = 'Driver'
        context['all_confirmed_bookings']= RentedVan.objects.filter(driver_id = driver_account, is_done=False, is_rejected=False, is_cancelled=False, is_confirmed=True).all()
    elif not passenger_account is None:
        context['profile'] = passenger_account
        context['account_type'] = 'Passenger'
        context['all_confirmed_bookings']= RentedVan.objects.filter(rented_by = passenger_account, is_done=False, is_rejected=False, is_cancelled=False, is_confirmed=True).all()


    if request.method == 'POST':
        cancel_booking_id = request.POST.get('cancel_booking_id')
        done_booking_id = request.POST.get('done_booking_id')
        enable_carpooling = request.POST.get('enable_carpooling')
        
        available_seats = request.POST.get('available_seats')
        from_destination_municipality  = request.POST.get('from_destination_municipality')
        to_destination_municipality  = request.POST.get('to_destination_municipality')
        from_destination_city  = request.POST.get('from_destination_city')
        to_destination_city  = request.POST.get('to_destination_city')

        
        if not cancel_booking_id is None:
            to_cancel_rent = RentedVan.objects.filter(id = cancel_booking_id).first()
            to_cancel_rent.is_cancelled = True
            to_cancel_rent.is_confirmed = False
            to_cancel_rent.save()

            driver = DriverAccount.objects.filter(id = to_cancel_rent.driver_id.id).first()
            driver.is_available = True
            driver.save()

            message_to_admin = f'CANCELLED || The rent booking with RENT ID : {to_cancel_rent.rent_id}, and destination FROM {to_cancel_rent.from_destination} TO {to_cancel_rent.to_destination} on {str(to_cancel_rent.travel_date)}'
            message_to_driver = f'CANCELLED || The rent booking with RENT ID : {to_cancel_rent.rent_id} where you have been assigned as a driver, with destination FROM {to_cancel_rent.from_destination} TO {to_cancel_rent.to_destination} on {str(to_cancel_rent.travel_date)}'
            message_to_passenger = f'CANCELLED || Your rent booking with RENT ID : {to_cancel_rent.rent_id}, with destination FROM {to_cancel_rent.from_destination} TO {to_cancel_rent.to_destination} on {str(to_cancel_rent.travel_date)}'
            
            create_notification(request, request.user, message_to_admin)
            create_notification(request, to_cancel_rent.driver_id.user_id, message_to_driver)
            create_notification(request, to_cancel_rent.rented_by.user_id, message_to_passenger)

            messages.info(request, f'The rent booking with RENT ID : {to_cancel_rent.rent_id} has been cancelled successfully.')
            return redirect('/confirmed-booking')
        
        elif not done_booking_id is None:
            done_rent = RentedVan.objects.filter(id = done_booking_id).first()
            done_rent.is_cancelled = False
            done_rent.is_confirmed = False
            done_rent.is_done = True
            done_rent.save()

            van = Van.objects.filter(id = done_rent.plate_no.id).first()

            create_tour_gallery = TourGallery.objects.create(rented_van = done_rent)
            create_tour_gallery.tour_gallery_id = f'GAL{create_tour_gallery.id}'
            create_tour_gallery.save()

            if enable_carpooling == "True":

                carpool_available_seats = None
                carpool_from_destination_city = None
                carpool_to_destination_city = None

                # get available seats
                if available_seats is None:
                    carpool_available_seats = van.number_of_seats
                else:
                    carpool_available_seats = int(available_seats)
                # get available seats
                
                # get from destination
                if from_destination_city is None:
                    carpool_from_destination_city = done_rent.to_destination
                else:
                    municipality = ListOfMunicipalities.objects.filter(id=from_destination_municipality).first()
                    city = ListOfDestinations.objects.filter(municipality = municipality, destination_name = from_destination_city).first()

                    carpool_from_destination_city = f'{city.destination_name}, {city.municipality.municipality_name}'
                # get from destination
                
                # get to destination
                if to_destination_city is None:
                    carpool_to_destination_city = done_rent.from_destination
                else:
                    municipality = ListOfMunicipalities.objects.filter(id=to_destination_municipality).first()
                    city = ListOfDestinations.objects.filter(municipality = municipality, destination_name = to_destination_city).first()

                    carpool_to_destination_city = f'{city.destination_name}, {city.municipality.municipality_name}'
                # get to destination


                create_carpool = CarpoolVan.objects.create(available_seat = carpool_available_seats,
                                                           from_destination = carpool_from_destination_city,
                                                           to_destination = carpool_to_destination_city,
                                                           plate_no = van,
                                                           driver_id = driver_account,
                                                           date_recorded = datetime.now())
                create_carpool.carpool_id = f'CPL{create_carpool.id}'
                create_carpool.save()

                message_to_admin = f'CARPOOL || Has been created with CARPOOL ID {create_carpool.carpool_id}, and destination FROM {create_carpool.from_destination} TO {create_carpool.to_destination}'
                message_to_driver = f'CARPOOL || Has been created with CARPOOL ID {create_carpool.carpool_id}, and destination FROM {create_carpool.from_destination} TO {create_carpool.to_destination}'
                
                create_notification(request, User.objects.filter(is_superuser = True).first(), message_to_admin)
                create_notification(request, driver_account.user_id, message_to_driver)

                messages.info(request, message_to_driver)
            else:

                message_to_admin = f'CARPOOL || Has not been created'
                message_to_driver = f'CARPOOL || Has not been created'

                create_notification(request, User.objects.filter(is_superuser = True).first(), message_to_admin)
                create_notification(request, driver_account.user_id, message_to_driver)
                
                messages.info(request, message_to_driver)


            message_to_admin = f'DONE || Boking with RENT ID : {done_rent.rent_id}, and destination FROM {done_rent.from_destination} TO {done_rent.to_destination} on {str(done_rent.travel_date)}'
            message_to_driver = f'DONE || Booking with RENT ID : {done_rent.rent_id} where you have been assigned as a driver, with destination FROM {done_rent.from_destination} TO {done_rent.to_destination} on {str(done_rent.travel_date)}'
            message_to_passenger = f'DONE || Your rent booking with RENT ID : {done_rent.rent_id}, with destination FROM {done_rent.from_destination} TO {done_rent.to_destination} on {str(done_rent.travel_date)}'
            message_to_driver_2 = 'GALLERY || A gallery for this tour has been created. Please check the gallery section for more info. Necessary files and information must be uploaded.'



            create_notification(request, request.user, message_to_admin)
            create_notification(request, done_rent.driver_id.user_id, message_to_driver)
            create_notification(request, done_rent.driver_id.user_id, message_to_driver_2)
            create_notification(request, done_rent.rented_by.user_id, message_to_passenger)

            messages.info(request, f'The rent booking with RENT ID : {done_rent.rent_id} has been marked as done successfully.')
            messages.info(request, message_to_driver_2)
            
            return redirect('/confirmed-booking')
        
    return render(request, 'vans/confirmed-booking.html', context)

############### FOR CARPOOLING PAGE
def available_carpooling(request):
    if not request.user.is_authenticated:
        messages.info(request, f'The page you are trying to access is not available.')
        return redirect('/login')
    
    if request.user.is_superuser:
        messages.info(request, f'The page you are trying to access is not available.')
        return redirect('/index')
    
    driver_account = DriverAccount.objects.filter(user_id = request.user).first()
    passenger_account = PassengerAccount.objects.filter(user_id = request.user).first()

    context = {}

    if not driver_account is None:
        context['profile'] = driver_account
        context['account_type'] = 'Driver'
        context['all_available_carpooling'] = CarpoolVan.objects.filter(driver_id = driver_account, is_done = False).all()

    elif not passenger_account is None:
        context['profile'] = passenger_account
        context['account_type'] = 'Passenger'
        context['all_available_carpooling'] = CarpoolVan.objects.filter(is_done = False).all()


    if request.method == 'POST':
        carpool_van_id  = request.POST.get('carpool_van_id')
        seats_occupied  = request.POST.get('seats_occupied')
        pick_up_location  = request.POST.get('pick_up_location')
        my_destination = request.POST.get('my_destination')

        booking_id  = request.POST.get('booking_id')
        is_rejected  = request.POST.get('is_rejected')
        is_approved  = request.POST.get('is_approved')

        is_dropped  = request.POST.get('is_dropped')
        passenger_fare = request.POST.get('passenger_fare')

        is_removed  = request.POST.get('is_removed')

        is_walkin = request.POST.get('is_walkin')
        walkin_van_id = request.POST.get('walkin_van_id')
        walkin_seats_occupied = request.POST.get('walkin_seats_occupied')
        walkin_pick_up_location = request.POST.get('walkin_pick_up_location')
        walkin_destination = request.POST.get('walkin_destination')

        cancel_my_booking = request.POST.get('cancel_my_booking')
        cancel_booking_id = request.POST.get('cancel_booking_id')

        mark_as_done_carpooling_id = request.POST.get('mark_as_done_carpooling_id')
        delete_or_remove_carpooling_id = request.POST.get('delete_or_remove_carpooling_id')

        if context['account_type'] == 'Passenger':
            if not carpool_van_id is None:
                carpool_van = CarpoolVan.objects.filter(id = carpool_van_id).first()
                seats_occupied = int(seats_occupied)

                if seats_occupied > int(carpool_van.available_seat):
                    messages.info(request, f'It seems like the seats that you will occupy exceeded the number of available seats in this carpooling!')
                    return redirect('/available-carpooling')
                
                else:
                    create_carpool_booking = BookedPassenger.objects.create(passenger_id = passenger_account,
                                                                            carpool_id = carpool_van,
                                                                            pick_up_location = pick_up_location,
                                                                            seats_occupied = seats_occupied,
                                                                            destination = my_destination)
                    create_carpool_booking.booked_id = f'BKDCPL{create_carpool_booking.id}'
                    create_carpool_booking.save()

                    message_to_driver = f'PLACED BOOKING || {passenger_account.user_id.first_name} {passenger_account.user_id.last_name} booked in your carpool, with PICK UP LOCATION {pick_up_location} and BOOKING ID : {create_carpool_booking.booked_id}'
                    message_to_passenger = f'PLACED BOOKING || You successfully booked in carpooling with CARPOOL ID : {carpool_van.carpool_id} and BOOKING ID : {create_carpool_booking.booked_id}. Please wait for the driver`s approval.'
                
                    create_notification(request, carpool_van.driver_id.user_id, message_to_driver)
                    create_notification(request, passenger_account.user_id, message_to_passenger)

                    messages.info(request, message_to_passenger)
                    return redirect('/available-carpooling')
            
            elif not cancel_my_booking is None:
                cancel_carpool_booking = BookedPassenger.objects.filter(id=cancel_booking_id).first()
                cancel_carpool_booking.is_cancelled = True
                cancel_carpool_booking.is_rejected = False
                cancel_carpool_booking.is_confirmed = False
                cancel_carpool_booking.is_dropped = False
                cancel_carpool_booking.date_cancelled = datetime.now()
                cancel_carpool_booking.save()

                message_to_driver = f'CANCELLED || A booking of a passenger has been cancelled with BOOKING ID : {cancel_carpool_booking.booked_id}'
                create_notification(request, request.user, message_to_driver)
                
                if not cancel_carpool_booking.passenger_id is None:
                    message_to_passenger = f'CANCELLED || You cancelled your carpool booking with BOOKING ID : {cancel_carpool_booking.booked_id}'
                    create_notification(request, cancel_carpool_booking.passenger_id.user_id, message_to_passenger)
                    messages.info(request, message_to_passenger)

                return redirect('/available-carpooling')

            
        elif context['account_type'] == 'Driver':
            if not is_approved is None:
                approve_carpool_booking = BookedPassenger.objects.filter(id=booking_id).first()
                approve_carpool_booking.is_confirmed = True
                approve_carpool_booking.is_rejected = False
                approve_carpool_booking.is_cancelled = False
                approve_carpool_booking.is_dropped = False
                approve_carpool_booking.date_confirmed = datetime.now()
                approve_carpool_booking.save()

                message_to_driver = f'APPROVED || You approved a carpool booking with BOOKING ID : {approve_carpool_booking.booked_id}'
                create_notification(request, request.user, message_to_driver)
                
                if not approve_carpool_booking.passenger_id is None:
                    message_to_passenger = f'APPROVED || Your carpool booking has been approved with BOOKING ID : {approve_carpool_booking.booked_id}'
                    create_notification(request, approve_carpool_booking.passenger_id.user_id, message_to_passenger)

                messages.info(request, message_to_driver)
                return redirect('/available-carpooling')


            elif not is_rejected is None:
                reject_carpool_booking = BookedPassenger.objects.filter(id=booking_id).first()
                reject_carpool_booking.is_rejected = True
                reject_carpool_booking.is_confirmed = False
                reject_carpool_booking.is_cancelled = False
                reject_carpool_booking.is_dropped = False
                reject_carpool_booking.date_rejected = datetime.now()
                reject_carpool_booking.save()

                message_to_driver = f'REJECTED || You rejected a carpool booking with BOOKING ID : {reject_carpool_booking.booked_id}'
                create_notification(request, request.user, message_to_driver)
                
                if not reject_carpool_booking.passenger_id is None:
                    message_to_passenger = f'REJECTED || Your carpool booking has been rejected with BOOKING ID : {reject_carpool_booking.booked_id}'
                    create_notification(request, reject_carpool_booking.passenger_id.user_id, message_to_passenger)

                messages.info(request, message_to_driver)
                return redirect('/available-carpooling')
            
            elif not is_dropped is None:
                dropped_passenger = BookedPassenger.objects.filter(id=booking_id).first()
                dropped_passenger.is_dropped = True
                dropped_passenger.is_confirmed = False
                dropped_passenger.is_rejected = False
                dropped_passenger.is_cancelled = False
                dropped_passenger.date_dropped = datetime.now()
                dropped_passenger.fare = passenger_fare
                dropped_passenger.save()

                message_to_driver = f'DROPPED || You dropped a passenger with BOOKING ID : {dropped_passenger.booked_id} and DESTINATION : {dropped_passenger.destination}'
                create_notification(request, request.user, message_to_driver)
                
                if not dropped_passenger.passenger_id is None:
                    message_to_passenger = f'DROPPED || The driver has been dropped you successfully in your DESTINATION : {dropped_passenger.destination}'
                    create_notification(request, dropped_passenger.passenger_id.user_id, message_to_passenger)

                messages.info(request, message_to_driver)
                return redirect('/available-carpooling')

            elif not is_removed is None:
                removed_passenger = BookedPassenger.objects.filter(id=booking_id).first()
                removed_passenger.is_confirmed = False
                removed_passenger.is_rejected = False
                removed_passenger.is_cancelled = False
                removed_passenger.is_dropped = False
    
                removed_passenger.date_confirmed = None
                removed_passenger.date_rejected = None
                removed_passenger.date_cancelled = None
                removed_passenger.date_dropped = None
                removed_passenger.save()

                message_to_driver = f'REMOVED || You removed a passenger from the confirmed booking with BOOKING ID : {removed_passenger.booked_id} and DESTINATION : {removed_passenger.destination}'
                create_notification(request, request.user, message_to_driver)
                
                if not removed_passenger.passenger_id is None:
                    message_to_passenger = f'REMOVED || The driver has been removed you from the list of Confirmed Bookings with your BOOKING ID : {removed_passenger.booked_id} and DESTINATION : {removed_passenger.destination}'
                    create_notification(request, removed_passenger.passenger_id.user_id, message_to_passenger)

                messages.info(request, message_to_driver)
                return redirect('/available-carpooling')
            
            elif not is_walkin is None:
                walkin_van = CarpoolVan.objects.filter(id = walkin_van_id).first()
        
                create_walkin_booking = BookedPassenger.objects.create(carpool_id = walkin_van,
                                                                        pick_up_location = walkin_pick_up_location,
                                                                        seats_occupied = walkin_seats_occupied,
                                                                        destination = walkin_destination,
                                                                        is_confirmed = True,
                                                                        date_confirmed = datetime.now())
                create_walkin_booking.booked_id = f'BKDCPL{create_walkin_booking.id}'
                create_walkin_booking.save()

                message_to_driver = f'PLACED BOOKING || A passenger has been picked up along the way, with PICK UP LOCATION {walkin_pick_up_location}, DESTINATION {walkin_destination}, and BOOKING ID : {create_walkin_booking.booked_id}'
            
                create_notification(request, walkin_van.driver_id.user_id, message_to_driver)

                messages.info(request, message_to_driver)
                return redirect('/available-carpooling')

            elif not mark_as_done_carpooling_id is None:
                carpool = CarpoolVan.objects.filter(id = mark_as_done_carpooling_id).first()
                carpool.is_done = True
                carpool.save()

                van = Van.objects.filter(id = carpool.plate_no.id).first()
                van.is_carpooled = False
                van.save()

                message_to_driver = f'DONE || You marked as done the carpooling with CARPOOLING ID : {carpool.carpool_id}'
                create_notification(request, request.user, message_to_driver)

                for booked_passenger in BookedPassenger.objects.filter(carpool_id = carpool, is_dropped = True).all():
                    if not booked_passenger.passenger_id is None:
                        message_to_passenger = f'DONE || The driver marked the carpooling with CARPOOLING ID : {carpool.carpool_id}. You can now post your review or comment!'
                        create_notification(request, booked_passenger.passenger_id.user_id, message_to_passenger)

                messages.info(request, message_to_driver)
                return redirect('/available-carpooling')
            
            elif not delete_or_remove_carpooling_id is None:
                carpool = CarpoolVan.objects.filter(id = delete_or_remove_carpooling_id).first()
                carpool.is_cancelled = True
                carpool.save()

                van = Van.objects.filter(id = carpool.plate_no.id).first()
                van.is_carpooled = False
                van.save()

                message_to_driver = f'CANCELLED || You cancelled a carpooling with CARPOOLING ID : {carpool.carpool_id}'
                create_notification(request, request.user, message_to_driver)

                for booked_passenger in BookedPassenger.objects.filter(carpool_id = carpool).all():
                    if not booked_passenger.passenger_id is None:
                        message_to_passenger = f'CANCELLED || The driver cancelled a carpooling with CARPOOLING ID : {carpool.carpool_id}'
                        create_notification(request, booked_passenger.passenger_id.user_id, message_to_passenger)

                messages.info(request, message_to_driver)
                return redirect('/available-carpooling')


    return render(request, 'vans/available-carpooling.html', context)


################ PAST CARPOOLING PAGE
def past_carpooling(request):
    if not request.user.is_authenticated:
        messages.info(request, f'The page you are trying to access is not available.')
        return redirect('/login')
    
    admin_account = AdminAccount.objects.filter(user_id = request.user).first()
    driver_account = DriverAccount.objects.filter(user_id = request.user).first()
    passenger_account = PassengerAccount.objects.filter(user_id = request.user).first()

    context = {}

    if not admin_account is None:
        context['profile'] = admin_account
        context['account_type'] = 'Admin'
        context['all_done_carpoolings'] = CarpoolVan.objects.filter(is_done=True).all()
    elif not driver_account is None:
        context['profile'] = driver_account
        context['account_type'] = 'Driver'
        context['all_done_carpoolings']= CarpoolVan.objects.filter(driver_id = driver_account, is_done=True).all()
    elif not passenger_account is None:
        context['profile'] = passenger_account
        context['account_type'] = 'Passenger'
        context['all_done_carpoolings']= CarpoolVan.objects.filter(is_done=True).all()

    if request.method == 'POST':
        done_carpooling_id = request.POST.get('done_carpooling_id')
        review_or_comment = request.POST.get('review_or_comment')
        rating = request.POST.get('rating')


        if context['account_type'] == 'Passenger':
            carpool = CarpoolVan.objects.filter(id = done_carpooling_id).first()
            carpool_booking = BookedPassenger.objects.filter(carpool_id = carpool, passenger_id = passenger_account).first()


            create_review = Review.objects.create(carpool_id = carpool_booking, 
                                                rating = rating, 
                                                comment = review_or_comment, 
                                                date_recorded = datetime.now())
            create_review.review_id = f'RVW{create_review.id}'
            create_review.save()

            message = 'You successfully posted a review!'
            create_notification(request, request.user, message)
            messages.info(request, message)
            return redirect('/past-carpooling')

    return render(request, 'vans/past-carpooling.html', context)


################ PAST BOOKING PAGE
def past_booking(request):

    if not request.user.is_authenticated:
        messages.info(request, f'The page you are trying to access is not available.')
        return redirect('/login')
    
    admin_account = AdminAccount.objects.filter(user_id = request.user).first()
    driver_account = DriverAccount.objects.filter(user_id = request.user).first()
    passenger_account = PassengerAccount.objects.filter(user_id = request.user).first()

    context = {}

    if not admin_account is None:
        context['profile'] = admin_account
        context['account_type'] = 'Admin'
        context['all_done_bookings'] = RentedVan.objects.filter(is_done=True).all()
    elif not driver_account is None:
        context['profile'] = driver_account
        context['account_type'] = 'Driver'
        context['all_done_bookings']= RentedVan.objects.filter(driver_id = driver_account, is_done=True).all()
    elif not passenger_account is None:
        context['profile'] = passenger_account
        context['account_type'] = 'Passenger'
        context['all_done_bookings']= RentedVan.objects.filter(rented_by = passenger_account, is_done=True).all()

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_or_comment = request.POST.get('review_or_comment')
        done_rent_id = request.POST.get('done_rent_id')

        create_review = Review.objects.create(rent_id = RentedVan.objects.filter(id=done_rent_id).first(), 
                                              rating = rating, 
                                              comment = review_or_comment, 
                                              date_recorded = datetime.now())
        create_review.review_id = f'RVW{create_review.id}'
        create_review.save()

        message = 'You successfully posted a review!'
        create_notification(request, request.user, message)
        messages.info(request, message)
        return redirect('/past-booking')

    return render(request, 'vans/past-booking.html', context)

    
################ MESSAGES PAGE
def user_messages(request):

    if not request.user.is_authenticated:
        messages.info(request, f'The page you are trying to access is not available.')
        return redirect('/login')
    

    return render(request, 'messages/messages.html')

################ MESSAGES PAGE
def filtered_messages(request, id):

    if not request.user.is_authenticated:
        messages.info(request, f'The page you are trying to access is not available.')
        return redirect('/login')
    
    else:

        convo_with = User.objects.filter(id=id).first()

        if not convo_with is None:
            all_messages = Messages.objects.filter((Q(sender = convo_with) & Q(receiver = request.user)) 
                                                    | (Q(sender= request.user) & Q(receiver = convo_with))).all().order_by('id')

            context = {
                'all_messages': all_messages,
                'convo_with' : convo_with,
                'messenger_name' : f'{convo_with.first_name} {convo_with.last_name}'
            }

            passenger_account = PassengerAccount.objects.filter(user_id = convo_with).first()
            driver_account = DriverAccount.objects.filter(user_id = convo_with).first()

            if passenger_account:
                context['message_sender'] = 'Passenger'
            elif driver_account:
                context['message_sender'] = 'Driver'
            else:
                context['message_sender'] = 'Admin'


            all_msg_is_seen = Messages.objects.filter(sender = convo_with, receiver = request.user, is_seen = False).all()

            for unseen_msg in all_msg_is_seen:
                Messages.objects.filter(id = unseen_msg.id).update(is_seen = True, date_seen = datetime.now())


            if request.method == 'POST':
                new_message = request.POST.get('new_message')

                if not new_message is None:
                    create_new_message = Messages.objects.create(sender = request.user,
                                                                receiver = convo_with,
                                                                date_sent = datetime.now(),
                                                                message = new_message)
                    create_new_message.message_id = f'MSG{create_new_message.id}'
                    create_new_message.save()

                    return redirect(f'/messages-{id}/')



            return render(request, 'messages/filtered-messages.html', context)

        else:
            messages.info(request, f'Sorry, we couldn`t find an account with ID {id}')
            return redirect('/messages')
        
    
################ GALLERY PAGE
def gallery(request):


    if request.method == 'POST':
        images = request.POST.get('images')
        title = request.POST.get('title')
        description = request.POST.get('description')
        gallery_id = request.POST.get('gallery_id')

        to_approve_gallery_id = request.POST.get('to_approve_gallery_id')

        to_heart_react_tour_id = request.POST.get('to_heart_react_tour_id')

        if images:
            images_list = images.split('|||')

            target_tour = TourGallery.objects.filter(id = gallery_id).first()
            target_tour.title = title
            target_tour.description = description
            target_tour.tour_gallery_id = f'TOUR{target_tour.id}'
            target_tour.is_modified = True
            target_tour.save()
            
            for img in images_list:
                new_gallery = TourGalleryImages.objects.create(tour_gallery = target_tour,
                                                               image = img)
                new_gallery.save()
            
            message_to_admin = f'PENDING GALLERY || {request.user.first_name} {request.user.last_name} added new gallery. It requires your approval. Please check it out!'
            message_to_driver = f'PENDING GALLERY || You added new gallery with title `{title}`. Waiting for the admin`s approval.'
                
            create_notification(request, User.objects.filter(is_superuser = True).first(), message_to_admin)
            create_notification(request, request.user, message_to_driver)

            messages.info(request, message_to_driver)

            return redirect('gallery')
        
        elif to_approve_gallery_id:
            to_approve = TourGallery.objects.filter(id = to_approve_gallery_id).first()
            to_approve.title = title
            to_approve.description = description
            to_approve.is_enabled = True
            to_approve.save()


            message_to_admin = f'APPROVED GALLERY || You successfully approved a gallery with title {title} and Gallery ID : {to_approve.tour_gallery_id}'
            message_to_driver = f'APPROVED GALLERY || The gallery for tour you uploaded with title {title} has been approved.'
                
            create_notification(request, request.user, message_to_admin)
            create_notification(request, to_approve.rented_van.driver_id.user_id, message_to_driver)

            messages.info(request, message_to_admin)
            return redirect('gallery')
        
        elif to_heart_react_tour_id:
            target_tour = TourGallery.objects.filter(id=to_heart_react_tour_id).first()

            if target_tour:
                heart_react_checker = HeartReactions.objects.filter(tour = target_tour, hearted_by = request.user).first()

                if heart_react_checker:

                    if heart_react_checker.is_hearted == True:
                        heart_react_checker.is_hearted = False
                    else:
                        messages.info(request,  f'You hearted the {target_tour.title}')
                        heart_react_checker.is_hearted = True
                    heart_react_checker.save()

                    return redirect('gallery')  
                
                else:
                    new_heart_react = HeartReactions.objects.create(tour = target_tour,
                                                                    hearted_by = request.user,
                                                                    is_hearted = True)
                    new_heart_react.save()

                    messages.info(request, f'You hearted the {target_tour.title}')                    
                    return redirect('gallery')  
            else:
                messages.info(request, 'Something went wrong. Please try again!')
                return redirect('gallery')  



    return render(request, 'gallery/gallery.html')



def filtered_gallery(request, id):

    context = {
        'tour_id' : id
    }
    # tour_gallery = TourGallery.objects.filter(id = id).first()
    
    # if tour_gallery:
    #     return render(request, 'gallery/filtered-gallery.html')
    
    # else:
    #     messages.info(request, f'Sorry, the gallery of a tour you want to visit is not available or doesn`t exist.')
    #     return redirect('/index')
    
    return render(request, 'gallery/filtered-gallery.html', context)


################ LOGOUT PAGE
def logout_page(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.info(request, 'Your account has been logged out successfully!')
        return redirect('/login')
    else:
        messages.info(request, 'It seems like you are trying to access an invalid page. Please login first')
        return redirect('/login')



# the admin must send auth_token to driver account



############################ THESE ARE USED FOR FETCHING USING JS ####################################################

################ GET PENDING DRIVER INFO PAGE
def get_pending_driver_info(request, id):
    driver_account = DriverAccount.objects.filter(user_id__id = id).first()
    
    if driver_account:
        driver_data = {
            'driver_id' : driver_account.driver_id,
            'email' : driver_account.user_id.email,
            'id' : driver_account.id
        }

        return JsonResponse(driver_data, safe=False)
    
    else:
        error = {
            'error' : 'Driver account not found'
        }
        return JsonResponse(json.dumps(error), status = 404)



def approve_pending_driver(request, id):
    driver_account = DriverAccount.objects.filter(user_id__id = id).first()
    
    if driver_account:
        auth_token = str(uuid.uuid4())
        driver_account.auth_token = auth_token
        driver_account.save()

        message = f'You successfully sent an email verification to {driver_account.user_id.first_name} {driver_account.user_id.first_name}! Please inform your driver about this update!'
        create_notification(request, request.user, message)

        return JsonResponse(message)
    
    else:
        message = f'Sorry, the system couldn`t find an account with User ID {id}'
        return JsonResponse(message)
    


def open_notification(request, id):
    notification = Notification.objects.filter(id = id).first()
    notification.is_seen = True
    notification.save()

    message_content = {
        'notification_id' : str(notification.notification_id),
        'message' : str(notification.message),
        'date_recorded' : str(notification.date_recorded),
        'messages' : 'You`ve seen this notification!'
    }

    return JsonResponse(message_content)


def rent_a_van(request, id):
    van = Van.objects.filter(id = id).first()

    all_images_container = []

    for van_image in VanImages.objects.filter(van_image_id = van).all():
        all_images_container.append(van_image.vehicle_image)

    response = {    
        'all_images' : all_images_container,
        'plate_no' : str(van.plate_no),
        # 'package_rent' : str(van.package_rent),
        'brand_name' : str(van.brand_name)
    }

    return JsonResponse(response)


def get_destination_address(request, id):
    destination_container = []

    for destination in ListOfDestinations.objects.filter(municipality__id = id).all():
        destination_container.append(destination.destination_name)

    response = {
        'destinations' : destination_container
    }

    return JsonResponse(response)


def get_carpooling_information(request, id):
    carpooling = CarpoolVan.objects.filter(id=id).first()
    all_booked_passengers = BookedPassenger.objects.filter(carpool_id = carpooling,
                                                           is_confirmed = True,
                                                           is_dropped = False).aggregate(all_booked_passengers = Sum('seats_occupied'))['all_booked_passengers']
    response = {}
    
    if not all_booked_passengers is None:
        remaining_available_seats = carpooling.available_seat - all_booked_passengers
        response['available_seats'] = remaining_available_seats
    else:
        response['available_seats'] = carpooling.available_seat

    all_images_container = []

    for van_image in VanImages.objects.filter(van_image_id = carpooling.plate_no).all():
        all_images_container.append(van_image.vehicle_image)

    response['all_images'] = all_images_container
    response['carpooling_id'] = carpooling.id
    response['from_destination'] = carpooling.from_destination
    response['to_destination'] = carpooling.to_destination

    return JsonResponse(response)



def get_chart_values(request, rentalOrCarpooling):


    admin_account = AdminAccount.objects.filter(user_id = request.user).first()
    driver_account = DriverAccount.objects.filter(user_id = request.user).first()
    passenger_account = PassengerAccount.objects.filter(user_id = request.user).first()

    response = {}

    list_of_months = ['Jan', 'Feb', 'Mar', 'Aprl', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    date_today = datetime.now()
    year_today = date_today.year


    ########## FOR ADMIN ##########
    if not admin_account is None:
        if rentalOrCarpooling == 'rental':
            temp_x_axis = []
            temp_y_axis = []

            for i in range(0, len(list_of_months)):
                all_rental = RentedVan.objects.filter(is_done = True, travel_date__year = year_today, travel_date__month = i + 1).count()
                temp_x_axis.append(all_rental)
                temp_y_axis.append(list_of_months[i])

            response['x_axis'] = temp_x_axis
            response['y_axis'] = temp_y_axis


        elif rentalOrCarpooling == 'carpooling':
            temp_x_axis = []
            temp_y_axis = []

            for i in range(0, len(list_of_months)):
                all_carpool = CarpoolVan.objects.filter(is_done = True, date_recorded__year = year_today, date_recorded__month = i + 1).count()
                temp_x_axis.append(all_carpool)
                temp_y_axis.append(list_of_months[i])

            response['x_axis'] = temp_x_axis
            response['y_axis'] = temp_y_axis
        
        else:
            temp_x_axis = []
            temp_y_axis = []

            for i in range(0, len(list_of_months)):
                all_carpool = CarpoolVan.objects.filter(is_done = True, date_recorded__year = year_today, date_recorded__month = i + 1).count()
                all_rental = RentedVan.objects.filter(is_done = True, travel_date__year = year_today, travel_date__month = i + 1).count()
                total = all_carpool + all_rental

                temp_x_axis.append(total)
                temp_y_axis.append(list_of_months[i])

            response['x_axis'] = temp_x_axis
            response['y_axis'] = temp_y_axis
    ########## FOR ADMIN ##########

    
    ########## FOR DRIVER ##########
    elif not driver_account is None:
        if rentalOrCarpooling == 'rental':
            temp_x_axis = []
            temp_y_axis = []

            for i in range(0, len(list_of_months)):
                all_rental = RentedVan.objects.filter(driver_id = driver_account, is_done = True, travel_date__year = year_today, travel_date__month = i + 1).count()

                temp_x_axis.append(all_rental)
                temp_y_axis.append(list_of_months[i])

            response['x_axis'] = temp_x_axis
            response['y_axis'] = temp_y_axis

        elif rentalOrCarpooling == 'carpooling':
            temp_x_axis = []
            temp_y_axis = []

            for i in range(0, len(list_of_months)):
                all_carpool = CarpoolVan.objects.filter(driver_id = driver_account, is_done = True, date_recorded__year = year_today, date_recorded__month = i + 1).count()

                temp_x_axis.append(all_carpool)
                temp_y_axis.append(list_of_months[i])

            response['x_axis'] = temp_x_axis
            response['y_axis'] = temp_y_axis
        
        else:
            temp_x_axis = []
            temp_y_axis = []

            for i in range(0, len(list_of_months)):
                all_carpool = CarpoolVan.objects.filter(driver_id = driver_account, is_done = True, date_recorded__year = year_today, date_recorded__month = i + 1).count()
                all_rental = RentedVan.objects.filter(driver_id = driver_account, is_done = True, travel_date__year = year_today, travel_date__month = i + 1).count()
                total = all_carpool + all_rental

                temp_x_axis.append(total)
                temp_y_axis.append(list_of_months[i])

            response['x_axis'] = temp_x_axis
            response['y_axis'] = temp_y_axis
    ########## FOR DRIVER ##########
    


    ########## FOR PASSENGER ##########
    elif not passenger_account is None:
        if rentalOrCarpooling == 'rental':
            temp_x_axis = []
            temp_y_axis = []

            for i in range(0, len(list_of_months)):
                all_rental = RentedVan.objects.filter(rented_by = passenger_account, is_done = True, travel_date__year = year_today, travel_date__month = i + 1).count()

                temp_x_axis.append(all_rental)
                temp_y_axis.append(list_of_months[i])

            response['x_axis'] = temp_x_axis
            response['y_axis'] = temp_y_axis

        elif rentalOrCarpooling == 'carpooling':
            temp_x_axis = []
            temp_y_axis = []

            for i in range(0, len(list_of_months)):
                all_carpool_booking = BookedPassenger.objects.filter(passenger_id = passenger_account, is_dropped = True, date_dropped__year = year_today, date_dropped__month = i + 1).count()

                temp_x_axis.append(all_carpool_booking)
                temp_y_axis.append(list_of_months[i])

            response['x_axis'] = temp_x_axis
            response['y_axis'] = temp_y_axis
        
        else:
            temp_x_axis = []
            temp_y_axis = []

            for i in range(0, len(list_of_months)):
                all_carpool_booking = BookedPassenger.objects.filter(passenger_id = passenger_account, is_dropped = True, date_dropped__year = year_today, date_dropped__month = i + 1).count()
                all_rental = RentedVan.objects.filter(rented_by = passenger_account, is_done = True, travel_date__year = year_today, travel_date__month = i + 1).count()
                total = all_carpool_booking + all_rental

                temp_x_axis.append(total)
                temp_y_axis.append(list_of_months[i])

            response['x_axis'] = temp_x_axis
            response['y_axis'] = temp_y_axis
    ########## FOR PASSENGER ##########
        
    

    return JsonResponse(response)




def get_unavailable_dates(request, id):
    rented_van = RentedVan.objects.filter(plate_no__id=id, is_confirmed = True, is_done = False).all()

    temp_storage = []
    for van in rented_van:
        # Start from the travel_date
        current_date = van.travel_date.date()

        # Loop until travel_date_end if it's not None
        while current_date <= (van.travel_date_end.date() if van.travel_date_end else van.travel_date.date()):
            # Format the date as "YYYY-MM-DD" string and append to the list
            formatted_date = current_date.strftime('%Y-%m-%d')
            temp_storage.append(formatted_date)
            
            # Move to the next day
            current_date += timedelta(days=1)

    # Convert the list to a JSON string
    return JsonResponse(temp_storage, safe=False)




def disable_gallery_image(request, id):

    target_image = TourGalleryImages.objects.filter(id=id).first()

    if target_image:
        target_image.is_enabled = False
        target_image.save()

        messsage = 'An image has been successfully disabled.'
        return JsonResponse(messsage, safe=False)
    
    else:
        messsage = 'Something went wrong. Please try again!'
        return JsonResponse(messsage, safe=False)




############################ THESE ARE USED FOR FETCHING USING JS ####################################################










# def add_municipality(request):
#     add_destinations(request)
#     return render(request, 'authentication/blank.html')



# @transaction.atomic
# def add_destinations(request):

#     # with transaction.atomic():
#     #     municipality = ['Quezon', 'Laguna', 'Rizal', 'Metro Manila', 'Cavite', 'Batangas', 'Benguet', 'Mountain Province', 'Isabela', 'Cagayan', 'Nueva Vizcaya', 'Nueva Ecija', 'Pangasinan', 'La Union']

#     #     x = 0
#     #     for i in municipality:
#     #         create_municipality = ListOfMunicipalities.objects.create(municipality_name = i)
#     #         create_municipality.save()
#     #         x = x + 1
        
#     #     return messages.info(request, f'{x} municipality saved')

#     # with transaction.atomic():
#     #     list_of_destinations = ["Lucban|| Quezon", "Lucena City|| Quezon", "Sta. Rosa|| Laguna", "Calamba|| Laguna", "Los Baños|| Laguna", "Binangonan|| Rizal", "Antipolo|| Rizal", "Angono|| Rizal", "Taytay|| Rizal", "Cainta|| Rizal", "Marikina City|| Metro Manila", "San Juan City|| Metro Manila", "Mandaluyong City|| Metro Manila", "Pasig City|| Metro Manila", "Quezon City|| Metro Manila", "Caloocan City|| Metro Manila", "Valenzuela City|| Metro Manila", "Malabon City|| Metro Manila", "Navotas City|| Metro Manila", "Manila City|| Metro Manila", "Makati City|| Metro Manila", "Taguig City|| Metro Manila", "Pasay City|| Metro Manila", "Parañaque City|| Metro Manila", "Las Piñas City|| Metro Manila", "Muntinlupa City|| Metro Manila", "Pateros|| Metro Manila", "San Pedro|| Laguna", "Biñan|| Laguna", "Cabuyao|| Laguna", "San Pablo City|| Laguna", "Calauan|| Laguna", "Santa Cruz|| Laguna", "Victoria|| Laguna", "Lumban|| Laguna", "Pila|| Laguna", "Bay|| Laguna", "Paete|| Laguna", "Pagsanjan|| Laguna", "Magdalena|| Laguna", "Mabitac|| Laguna", "Siniloan|| Laguna", "Famy|| Laguna", "Luisiana|| Laguna", "Pakil|| Laguna", "Nagcarlan|| Laguna", "Rizal|| Laguna", "Santa Maria|| Laguna", "Liliw|| Laguna", "Sta. Cruz|| Laguna", "Carmona|| Cavite", "Cavite City|| Cavite", "Tagaytay City|| Cavite", "Dasmariñas City|| Cavite", "Trece Martires City|| Cavite", "Imus City|| Cavite", "Bacoor City|| Cavite", "General Trias City|| Cavite", "Noveleta|| Cavite", "Kawit|| Cavite", "Rosario|| Cavite", "Tanza|| Cavite", "Naic|| Cavite", "Amadeo|| Cavite", "Gen. Mariano Alvarez|| Cavite", "Indang|| Cavite", "Silang|| Cavite", "Maragondon|| Cavite", "Ternate|| Cavite", "Alfonso|| Cavite", "Magallanes|| Cavite", "Cuenca|| Batangas", "San Juan|| Batangas", "Balayan|| Batangas", "Tuy|| Batangas", "Nasugbu|| Batangas", "Calatagan|| Batangas", "Lian|| Batangas", "Laurel|| Batangas", "Talisay|| Batangas", "San Jose|| Batangas", "Lipa City|| Batangas", "Tanauan City|| Batangas", "Sto. Tomas City|| Batangas", "Malvar|| Batangas", "Ibaan|| Batangas", "Batangas City|| Batangas", "Lobo|| Batangas", "Tingloy|| Batangas", "San Pascual|| Batangas", "Bauan|| Batangas", "Mabini|| Batangas", "Padre Garcia|| Batangas", "San Luis|| Batangas", "Agoncillo|| Batangas", "San Nicolas|| Batangas", "Taal|| Batangas", "Santa Teresita|| Batangas", "Rosario|| Batangas", "Balete|| Batangas", "Sto. Tomas|| Batangas", "Lemery|| Batangas", "Calaca|| Batangas", "Baguio City|| Benguet", "La Trinidad|| Benguet", "Itogon|| Benguet", "Tuba|| Benguet", "Tublay|| Benguet", "Bokod|| Benguet", "Kabayan|| Benguet", "Atok|| Benguet", "Kapangan|| Benguet", "Bauko|| Mountain Province", "Bontoc|| Mountain Province", "Sadanga|| Mountain Province", "Sabangan|| Mountain Province", "Sagada|| Mountain Province", "Besao|| Mountain Province", "Tadian|| Mountain Province", "Barlig|| Mountain Province", "Paracelis|| Mountain Province", "Cauayan City|| Isabela", "Ilagan City|| Isabela", "Santiago City|| Isabela", "Aurora|| Isabela", "Cabagan|| Isabela", "Tuguegarao City|| Cagayan", "Aparri|| Cagayan", "Lal-lo|| Cagayan", "Gattaran|| Cagayan", "Santa Ana|| Cagayan", "Enrile|| Cagayan", "Peñablanca|| Cagayan", "Solana|| Cagayan", "Rizal|| Cagayan", "Baggao|| Cagayan", "Alcala|| Cagayan", "Iguig|| Cagayan", "Calayan|| Cagayan", "Bambang|| Nueva Vizcaya", "Bayombong|| Nueva Vizcaya", "Solano|| Nueva Vizcaya", "Bagabag|| Nueva Vizcaya", "Diadi|| Nueva Vizcaya", "Kayapa|| Nueva Vizcaya", "Quezon|| Nueva Vizcaya", "Santa Fe|| Nueva Vizcaya", "Villaverde|| Nueva Vizcaya", "Dupax del Norte|| Nueva Vizcaya", "Dupax del Sur|| Nueva Vizcaya", "Santo Domingo|| Nueva Ecija", "Cabiao|| Nueva Ecija", "San Isidro|| Nueva Ecija", "Aliaga|| Nueva Ecija", "Licab|| Nueva Ecija", "Zaragoza|| Nueva Ecija", "Talavera|| Nueva Ecija", "Guimba|| Nueva Ecija", "Quezon|| Nueva Ecija", "Cabanatuan City|| Nueva Ecija", "Palayan City|| Nueva Ecija", "Gapan City|| Nueva Ecija", "Muñoz City|| Nueva Ecija", "San Jose City|| Nueva Ecija", "Santa Rosa|| Nueva Ecija", "San Leonardo|| Nueva Ecija", "Peñaranda|| Nueva Ecija", "Talugtug|| Nueva Ecija", "Roxas|| Isabela", "San Manuel|| Isabela", "Benito Soliven|| Isabela", "Naguilian|| Isabela", "Reina Mercedes|| Isabela", "Alicia|| Isabela", "Angadanan|| Isabela", "San Guillermo|| Isabela", "San Mateo|| Isabela", "Jones|| Isabela", "San Agustin|| Isabela", "San Isidro|| Isabela", "Echague|| Isabela", "San Mariano|| Isabela", "Ramón|| Isabela", "Cordon|| Isabela", "Luna|| Isabela", "Cabatuan|| Isabela", "Maconacon|| Isabela", "Delfin Albano|| Isabela", "Tumauini|| Isabela", "Santa Maria|| Isabela", "San Pablo|| Isabela", "Tayug|| Pangasinan", "Umingan|| Pangasinan", "Balungao|| Pangasinan", "Binalonan|| Pangasinan", "San Manuel|| Pangasinan", "Asingan|| Pangasinan", "Urdaneta City|| Pangasinan", "Sison|| Pangasinan", "Pozorrubio|| Pangasinan", "Lingayen|| Pangasinan", "Dagupan City|| Pangasinan", "San Carlos City|| Pangasinan", "Alaminos City|| Pangasinan", "Bayambang|| Pangasinan", "Basista|| Pangasinan", "Bautista|| Pangasinan", "Malasiqui|| Pangasinan", "Villasis|| Pangasinan", "Sual|| Pangasinan", "Pozzorubio|| Pangasinan", "Mangaldan|| Pangasinan", "San Fabian|| Pangasinan", "Rosales|| Pangasinan", "Sta. Maria|| Pangasinan", "Manaoag|| Pangasinan", "Calasiao|| Pangasinan", "Binmaley|| Pangasinan", "Laoac|| Pangasinan", "San Quintin|| Pangasinan", "Mangatarem|| Pangasinan", "Aguilar|| Pangasinan", "Bugallon|| Pangasinan", "Infanta|| Pangasinan", "Dasol|| Pangasinan", "Mabini|| Pangasinan", "Burgos|| Pangasinan", "Alcala|| Pangasinan", "San Jacinto|| Pangasinan", "Bani|| Pangasinan", "Santo Tomas|| Pangasinan", "Santa Barbara|| Pangasinan", "Agoo|| La Union", "Aringay|| La Union", "Bacnotan|| La Union", "Bagulin|| La Union", "Balaoan|| La Union", "Bangar|| La Union", "Bauang|| La Union", "Burgos|| La Union", "Caba|| La Union", "Luna|| La Union", "Naguilian|| La Union", "Pugo|| La Union", "Rosario|| La Union", "San Fernando City|| La Union", "San Gabriel|| La Union", "San Juan|| La Union", "Santo Tomas|| La Union", "Santol|| La Union", "Sudipen|| La Union", "Tubao|| La Union", "Santa Maria|| Pangasinan", "San Nicolas|| Pangasinan"]

#     #     x = 0
#     #     for destination in list_of_destinations:
#     #         sliced = destination.split('|| ')

#     #         municipality = ListOfMunicipalities.objects.filter(municipality_name = sliced[1]).first()

#     #         create_destination = ListOfDestinations.objects.create(municipality = municipality, destination_name = sliced[0])
#     #         create_destination.save()

#     #         x = x + 1

#         # return messages.info(request, f'{x} destination saved')
    
#     return messages.info(request, f'something went wrong')
