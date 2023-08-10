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
# Create your views here.

def RemoveSpaces(name):
    li = list(name.split(" "))
    temp_container = ''.join(li)

    return temp_container
            
def create_notification(request, user_id, message):
    create_notif = Notification.objects.create(receiver_id = user_id,
                                                        message = message,
                                                        date_recorded = datetime.now())
    create_notif.notification_id = f'NOTF{create_notif.id}'
    create_notif.save()


def index(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        loginAccount(request, username, password)

    return render(request, 'homepage/index.html')

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

################ LOGIN PAGE
def login_page(request):
    if request.user.is_authenticated:
        messages.info(request, 'The page you are trying to access is not available because you are already logged in!')
        return redirect('/index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        loginAccount(request, username, password)

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

            messages.info(request, f'An email verification is sent to {driver_account.user_id.first_name} {driver_account.user_id.first_name} with email {driver_account.user_id.email}. If you want to contact him, use this number ({driver_account.contact_no})')
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


    
############################ THESE ARE USED FOR FETCHING USING JS ####################################################
