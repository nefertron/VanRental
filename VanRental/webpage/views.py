from django.shortcuts import render, redirect

from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from datetime import datetime
import uuid

from django.conf import settings
from django.core.mail import send_mail

# Create your views here.


def index(request):

    return render(request, 'homepage/index.html')


################ LOGIN PAGE
def login_page(request):
    if request.user.is_authenticated:
        messages.info(request, 'The page you are trying to access is not available because you are already logged in!')
        return redirect('/index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        def UsernameConverter(username):
                li = list(username.split(" "))
                return li
        temp_username_id = UsernameConverter(username.lower())
        username = ''.join(temp_username_id)

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
            def UsernameConverter(username):
                li = list(username.split(" "))
                return li
            
            temp_username = UsernameConverter(username.lower())
            username = ''.join(temp_username)

            temp_email = UsernameConverter(email.lower())
            email = ''.join(temp_email)
        
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
    message = f'Thank you for signing up on our page.\nPlease click the link below to complete the account activation process.\nhttps://{host}/verify/{account_type}/{auth_token}'
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
            return redirect('/login')
        else:
            messages.info(request, f'Sorry, the page you are trying to access is invalid or expired. Please try another!')
            return redirect('/login')




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