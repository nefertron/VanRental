from django.shortcuts import render, redirect

from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from datetime import datetime
import uuid

from django.conf import settings
from django.core.mail import send_mail

from django.http import JsonResponse
from json import dumps
import json

from django.db import transaction
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
                return redirect('/login')
            else:
                passenger_account = PassengerAccount.objects.filter(user_id = user, is_verified = True).first()
                admin_account = AdminAccount.objects.filter(user_id = user, is_verified = True).first()
                driver_account = DriverAccount.objects.filter(user_id = user, is_verified = True).first()
                if passenger_account or admin_account or driver_account:
                    login(request, user)
                    messages.info(request, 'You logged in successfully!')
                    return redirect('/index')
                else:
                    if passenger_account:
                        messages.info(request, 'It seems like your account is not verified yet. Please check your email for the verification')
                    else:
                        messages.info(request, 'It seems like your account is not verified yet. Please contact the administrator to verify your account!')
                    return redirect('/login')
        else:
            messages.info(request, f'Sorry, we couldn`t find an account with email {username}!')

    else:
        user = User.objects.filter(username = username).first()
        if user:
            to_login = authenticate(username = username, password = password)
            if to_login is None:
                messages.info(request, 'Sorry, the password you entered is invalid. Please try again!')
                return redirect('/login')
            else:
                passenger_account = PassengerAccount.objects.filter(user_id = user, is_verified = True).first()
                admin_account = AdminAccount.objects.filter(user_id = user, is_verified = True).first()
                driver_account = DriverAccount.objects.filter(user_id = user, is_verified = True).first()
                if passenger_account or admin_account or driver_account:
                    login(request, user)
                    messages.info(request, 'You logged in successfully!')
                    return redirect('/index')
                else:
                    if passenger_account:
                        messages.info(request, 'It seems like your account is not verified yet. Please check your email for the verification')
                    else:
                        messages.info(request, 'It seems like your account is not verified yet. Please contact the administrator to verify your account!')
                    return redirect('/login')
        else:
            messages.info(request, f'Sorry, we couldn`t find an account with username {username}!')

################ REUSABLE BOOKING DEF FUNCTION


################ HOME PAGE
def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        package_rent = request.POST.get('package_rent')
        van_id = request.POST.get('van_id')
        from_destination_municipality_id = request.POST.get('from_destination_municipality')
        from_destination = request.POST.get('from_destination')
        to_destination_municipality_id = request.POST.get('to_destination_municipality')
        to_destination = request.POST.get('to_destination')
        travel_date = request.POST.get('travel_date')


        if username and password:
            loginAccount(request, username, password)
        
        else:
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

            van = Van.objects.filter(id = create_rent_van.plate_no.id).first()
            van.is_rented = True
            van.save()

            message = f'You successfully set a booking. Please wait for the confirmation of the admin. Please note that the rent is subjected to an adjustment.'
            create_notification(request, request.user, message)

            admin_account = User.objects.filter(is_superuser = True).first()
            message_to_admin = f'{request.user.first_name} {request.user.last_name} set a booking with a scheduled date {travel_date}. Please visit the booking section for more details.'
            create_notification(request, admin_account, message_to_admin)

            return redirect('/confirmed-booking')


    return render(request, 'homepage/index.html')

################ LOGIN PAGE
def login_page(request):
    if request.user.is_authenticated:
        messages.info(request, 'The page you are trying to access is not available because you are already logged in!')
        return redirect('/index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        loginAccount(request, username, password)

        return redirect('/index')
    
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
        username = request.POST.get('username')
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
        
        elif User.objects.filter(username = username).count() > 1:
            messages.info(request, f'Sorry, the username you entered is not available. Please try another!')
            return redirect('/profile')

        else:
            username = RemoveSpaces(username.lower())
            email = RemoveSpaces(email.lower())

            all_changes = []

            if username != context["profile"].user_id.username:
                all_changes.append('username')
            
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

            User.objects.filter().update(first_name = fname,
                                        last_name = lname,
                                        email = email,
                                        username = username)

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




################ LOGOUT PAGE
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

        image_list = images.split('|||') # use to split the image addresses generated by the javascript
        plate_no = RemoveSpaces(plate_no)

        if Van.objects.filter(plate_no = plate_no).first():
            messages.info(request, f'It seems like the Plate No. you entered is already existing, perhaps you made a mistake?')
            return redirect('/list-of-vans')
        
        else:
            if len(image_list) > 0:
                new_van = Van.objects.create(plate_no = plate_no, 
                                             color = color, 
                                             number_of_seats = number_of_seats, 
                                             description = description,
                                             brand_name = brand_name)
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

        booking_target = RentedVan.objects.filter(id = booking_id).first()
        driver_target = DriverAccount.objects.filter(id = driver_id).first()

        booking_target.driver_id = driver_target
        booking_target.is_confirmed = True
        booking_target.save()

        message_to_admin = f'You confirmed a rent booking with RENT ID : {booking_target.rent_id}, with destination FROM {booking_target.from_destination} TO {booking_target.to_destination} on {booking_target.travel_date.date}'
        message_to_driver = f'You have been assigned as a driver in a rent booking with RENT ID : {booking_target.rent_id}, with destination FROM {booking_target.from_destination} TO {booking_target.to_destination} on {booking_target.travel_date.date}'
        message_to_passenger = f'Your rent booking with RENT ID : {booking_target.rent_id} has been confirmed, with destination FROM {booking_target.from_destination} TO {booking_target.to_destination} on {booking_target.travel_date.date}'
        
        driver_target.is_available = False
        driver_target.save()


        van = Van.objects.filter(id = booking_target.plate_no.id).first()
        van.is_rented = True
        van.save()

        create_notification(request, request.user, message_to_admin)
        create_notification(request, driver_target.user_id, message_to_driver)
        create_notification(request, booking_target.rented_by.user_id, message_to_passenger)

        messages.info(request, message_to_admin)
        return redirect('/rent-booking')

    return render(request, 'vans/rent-booking.html', context)



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

        if not cancel_booking_id is None:
            to_cancel_rent = RentedVan.objects.filter(id = cancel_booking_id).first()
            to_cancel_rent.is_cancelled = True
            to_cancel_rent.is_confirmed = False
            to_cancel_rent.save()

            driver = DriverAccount.objects.filter(id = to_cancel_rent.driver_id.id).first()
            driver.is_available = True
            driver.save()

            van = Van.objects.filter(id = to_cancel_rent.plate_no.id).first()
            van.is_rented = False
            van.save()
            
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

            driver = DriverAccount.objects.filter(id = done_rent.driver_id.id).first()
            driver.is_available = True
            driver.save()
            
            van = Van.objects.filter(id = done_rent.plate_no.id).first()
            van.is_rented = False
            van.save()

            message_to_admin = f'DONE || Boking with RENT ID : {done_rent.rent_id}, and destination FROM {done_rent.from_destination} TO {done_rent.to_destination} on {str(done_rent.travel_date)}'
            message_to_driver = f'DONE || Booking with RENT ID : {done_rent.rent_id} where you have been assigned as a driver, with destination FROM {done_rent.from_destination} TO {done_rent.to_destination} on {str(done_rent.travel_date)}'
            message_to_passenger = f'DONE || Your rent booking with RENT ID : {done_rent.rent_id}, with destination FROM {done_rent.from_destination} TO {done_rent.to_destination} on {str(done_rent.travel_date)}'
            
            create_notification(request, request.user, message_to_admin)
            create_notification(request, done_rent.driver_id.user_id, message_to_driver)
            create_notification(request, done_rent.rented_by.user_id, message_to_passenger)

            messages.info(request, f'The rent booking with RENT ID : {done_rent.rent_id} has been marked as done successfully.')
            return redirect('/confirmed-booking')
        
    return render(request, 'vans/confirmed-booking.html', context)



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

    return render(request, 'vans/past-booking.html', context)

    



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
        'package_rent' : str(van.package_rent),
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


    
############################ THESE ARE USED FOR FETCHING USING JS ####################################################










def add_municipality(request):
    add_destinations(request)
    return render(request, 'authentication/blank.html')



@transaction.atomic
def add_destinations(request):

    # with transaction.atomic():
    #     municipality = ['Quezon', 'Laguna', 'Rizal', 'Metro Manila', 'Cavite', 'Batangas', 'Benguet', 'Mountain Province', 'Isabela', 'Cagayan', 'Nueva Vizcaya', 'Nueva Ecija', 'Pangasinan', 'La Union']

    #     x = 0
    #     for i in municipality:
    #         create_municipality = ListOfMunicipalities.objects.create(municipality_name = i)
    #         create_municipality.save()
    #         x = x + 1
        
    #     return messages.info(request, f'{x} municipality saved')

    # with transaction.atomic():
    #     list_of_destinations = ["Lucban|| Quezon", "Lucena City|| Quezon", "Sta. Rosa|| Laguna", "Calamba|| Laguna", "Los Baños|| Laguna", "Binangonan|| Rizal", "Antipolo|| Rizal", "Angono|| Rizal", "Taytay|| Rizal", "Cainta|| Rizal", "Marikina City|| Metro Manila", "San Juan City|| Metro Manila", "Mandaluyong City|| Metro Manila", "Pasig City|| Metro Manila", "Quezon City|| Metro Manila", "Caloocan City|| Metro Manila", "Valenzuela City|| Metro Manila", "Malabon City|| Metro Manila", "Navotas City|| Metro Manila", "Manila City|| Metro Manila", "Makati City|| Metro Manila", "Taguig City|| Metro Manila", "Pasay City|| Metro Manila", "Parañaque City|| Metro Manila", "Las Piñas City|| Metro Manila", "Muntinlupa City|| Metro Manila", "Pateros|| Metro Manila", "San Pedro|| Laguna", "Biñan|| Laguna", "Cabuyao|| Laguna", "San Pablo City|| Laguna", "Calauan|| Laguna", "Santa Cruz|| Laguna", "Victoria|| Laguna", "Lumban|| Laguna", "Pila|| Laguna", "Bay|| Laguna", "Paete|| Laguna", "Pagsanjan|| Laguna", "Magdalena|| Laguna", "Mabitac|| Laguna", "Siniloan|| Laguna", "Famy|| Laguna", "Luisiana|| Laguna", "Pakil|| Laguna", "Nagcarlan|| Laguna", "Rizal|| Laguna", "Santa Maria|| Laguna", "Liliw|| Laguna", "Sta. Cruz|| Laguna", "Carmona|| Cavite", "Cavite City|| Cavite", "Tagaytay City|| Cavite", "Dasmariñas City|| Cavite", "Trece Martires City|| Cavite", "Imus City|| Cavite", "Bacoor City|| Cavite", "General Trias City|| Cavite", "Noveleta|| Cavite", "Kawit|| Cavite", "Rosario|| Cavite", "Tanza|| Cavite", "Naic|| Cavite", "Amadeo|| Cavite", "Gen. Mariano Alvarez|| Cavite", "Indang|| Cavite", "Silang|| Cavite", "Maragondon|| Cavite", "Ternate|| Cavite", "Alfonso|| Cavite", "Magallanes|| Cavite", "Cuenca|| Batangas", "San Juan|| Batangas", "Balayan|| Batangas", "Tuy|| Batangas", "Nasugbu|| Batangas", "Calatagan|| Batangas", "Lian|| Batangas", "Laurel|| Batangas", "Talisay|| Batangas", "San Jose|| Batangas", "Lipa City|| Batangas", "Tanauan City|| Batangas", "Sto. Tomas City|| Batangas", "Malvar|| Batangas", "Ibaan|| Batangas", "Batangas City|| Batangas", "Lobo|| Batangas", "Tingloy|| Batangas", "San Pascual|| Batangas", "Bauan|| Batangas", "Mabini|| Batangas", "Padre Garcia|| Batangas", "San Luis|| Batangas", "Agoncillo|| Batangas", "San Nicolas|| Batangas", "Taal|| Batangas", "Santa Teresita|| Batangas", "Rosario|| Batangas", "Balete|| Batangas", "Sto. Tomas|| Batangas", "Lemery|| Batangas", "Calaca|| Batangas", "Baguio City|| Benguet", "La Trinidad|| Benguet", "Itogon|| Benguet", "Tuba|| Benguet", "Tublay|| Benguet", "Bokod|| Benguet", "Kabayan|| Benguet", "Atok|| Benguet", "Kapangan|| Benguet", "Bauko|| Mountain Province", "Bontoc|| Mountain Province", "Sadanga|| Mountain Province", "Sabangan|| Mountain Province", "Sagada|| Mountain Province", "Besao|| Mountain Province", "Tadian|| Mountain Province", "Barlig|| Mountain Province", "Paracelis|| Mountain Province", "Cauayan City|| Isabela", "Ilagan City|| Isabela", "Santiago City|| Isabela", "Aurora|| Isabela", "Cabagan|| Isabela", "Tuguegarao City|| Cagayan", "Aparri|| Cagayan", "Lal-lo|| Cagayan", "Gattaran|| Cagayan", "Santa Ana|| Cagayan", "Enrile|| Cagayan", "Peñablanca|| Cagayan", "Solana|| Cagayan", "Rizal|| Cagayan", "Baggao|| Cagayan", "Alcala|| Cagayan", "Iguig|| Cagayan", "Calayan|| Cagayan", "Bambang|| Nueva Vizcaya", "Bayombong|| Nueva Vizcaya", "Solano|| Nueva Vizcaya", "Bagabag|| Nueva Vizcaya", "Diadi|| Nueva Vizcaya", "Kayapa|| Nueva Vizcaya", "Quezon|| Nueva Vizcaya", "Santa Fe|| Nueva Vizcaya", "Villaverde|| Nueva Vizcaya", "Dupax del Norte|| Nueva Vizcaya", "Dupax del Sur|| Nueva Vizcaya", "Santo Domingo|| Nueva Ecija", "Cabiao|| Nueva Ecija", "San Isidro|| Nueva Ecija", "Aliaga|| Nueva Ecija", "Licab|| Nueva Ecija", "Zaragoza|| Nueva Ecija", "Talavera|| Nueva Ecija", "Guimba|| Nueva Ecija", "Quezon|| Nueva Ecija", "Cabanatuan City|| Nueva Ecija", "Palayan City|| Nueva Ecija", "Gapan City|| Nueva Ecija", "Muñoz City|| Nueva Ecija", "San Jose City|| Nueva Ecija", "Santa Rosa|| Nueva Ecija", "San Leonardo|| Nueva Ecija", "Peñaranda|| Nueva Ecija", "Talugtug|| Nueva Ecija", "Roxas|| Isabela", "San Manuel|| Isabela", "Benito Soliven|| Isabela", "Naguilian|| Isabela", "Reina Mercedes|| Isabela", "Alicia|| Isabela", "Angadanan|| Isabela", "San Guillermo|| Isabela", "San Mateo|| Isabela", "Jones|| Isabela", "San Agustin|| Isabela", "San Isidro|| Isabela", "Echague|| Isabela", "San Mariano|| Isabela", "Ramón|| Isabela", "Cordon|| Isabela", "Luna|| Isabela", "Cabatuan|| Isabela", "Maconacon|| Isabela", "Delfin Albano|| Isabela", "Tumauini|| Isabela", "Santa Maria|| Isabela", "San Pablo|| Isabela", "Tayug|| Pangasinan", "Umingan|| Pangasinan", "Balungao|| Pangasinan", "Binalonan|| Pangasinan", "San Manuel|| Pangasinan", "Asingan|| Pangasinan", "Urdaneta City|| Pangasinan", "Sison|| Pangasinan", "Pozorrubio|| Pangasinan", "Lingayen|| Pangasinan", "Dagupan City|| Pangasinan", "San Carlos City|| Pangasinan", "Alaminos City|| Pangasinan", "Bayambang|| Pangasinan", "Basista|| Pangasinan", "Bautista|| Pangasinan", "Malasiqui|| Pangasinan", "Villasis|| Pangasinan", "Sual|| Pangasinan", "Pozzorubio|| Pangasinan", "Mangaldan|| Pangasinan", "San Fabian|| Pangasinan", "Rosales|| Pangasinan", "Sta. Maria|| Pangasinan", "Manaoag|| Pangasinan", "Calasiao|| Pangasinan", "Binmaley|| Pangasinan", "Laoac|| Pangasinan", "San Quintin|| Pangasinan", "Mangatarem|| Pangasinan", "Aguilar|| Pangasinan", "Bugallon|| Pangasinan", "Infanta|| Pangasinan", "Dasol|| Pangasinan", "Mabini|| Pangasinan", "Burgos|| Pangasinan", "Alcala|| Pangasinan", "San Jacinto|| Pangasinan", "Bani|| Pangasinan", "Santo Tomas|| Pangasinan", "Santa Barbara|| Pangasinan", "Agoo|| La Union", "Aringay|| La Union", "Bacnotan|| La Union", "Bagulin|| La Union", "Balaoan|| La Union", "Bangar|| La Union", "Bauang|| La Union", "Burgos|| La Union", "Caba|| La Union", "Luna|| La Union", "Naguilian|| La Union", "Pugo|| La Union", "Rosario|| La Union", "San Fernando City|| La Union", "San Gabriel|| La Union", "San Juan|| La Union", "Santo Tomas|| La Union", "Santol|| La Union", "Sudipen|| La Union", "Tubao|| La Union", "Santa Maria|| Pangasinan", "San Nicolas|| Pangasinan"]

    #     x = 0
    #     for destination in list_of_destinations:
    #         sliced = destination.split('|| ')

    #         municipality = ListOfMunicipalities.objects.filter(municipality_name = sliced[1]).first()

    #         create_destination = ListOfDestinations.objects.create(municipality = municipality, destination_name = sliced[0])
    #         create_destination.save()

    #         x = x + 1

        # return messages.info(request, f'{x} destination saved')
    
    return messages.info(request, f'something went wrong')
