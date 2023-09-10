from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from datetime import datetime

class AdminAccount(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    bday = models.DateField()
    contact_no = models.CharField(max_length=13)
    address = models.TextField()
    auth_token = models.CharField(max_length=50, null=True, blank=True)
    profile = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user_id.first_name} {self.user_id.last_name}'
    

class DriverAccount(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    driver_id = models.CharField(max_length=15)
    bday = models.DateField()
    contact_no = models.CharField(max_length=13)
    address = models.TextField()
    is_verified = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=50, null=True, blank=True)
    profile = models.TextField(null=True, blank=True)

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user_id.first_name} {self.user_id.last_name}'
    

class PassengerAccount(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    passenger_id = models.CharField(max_length=15)
    bday = models.DateField()
    contact_no = models.CharField(max_length=13)
    address = models.TextField()
    is_verified = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=50, null=True, blank=True)
    profile = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user_id.first_name} {self.user_id.last_name}'
    

class Notification(models.Model):
    notification_id = models.CharField(max_length=20)
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    date_recorded = models.DateTimeField(default=datetime.now())
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f'Receiver : {self.receiver_id.first_name} || Is Seen : {self.is_seen}'
    


class Van(models.Model):
    brand_name = models.CharField(max_length=20, default=None, blank=True, null=True)
    plate_no = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    number_of_seats = models.IntegerField(default=0)
    description = models.TextField(default=None, null=True, blank=True)
    is_airconditioned =  models.BooleanField(default=True, blank=True, null=True)
    is_rented = models.BooleanField(default=False)
    is_carpooled = models.BooleanField(default=False)
    package_rent = models.IntegerField(default=0)

    def __str__(self):
        return f'PLATE NO. : {self.plate_no} || COLOR : {self.color}'
    

class VanImages(models.Model):
    van_image_id = models.ForeignKey(Van, on_delete=models.CASCADE)
    vehicle_image = models.TextField()

    def __str__(self):
        return f'PLATE NO : {self.van_image_id.plate_no}'


class RentedVan(models.Model):
    rent_id = models.CharField(max_length=20)
    plate_no = models.ForeignKey(Van, on_delete=models.CASCADE)
    driver_id = models.ForeignKey(DriverAccount, on_delete=models.CASCADE, default=None, blank=True, null=True)
    rented_by = models.ForeignKey(PassengerAccount, on_delete=models.CASCADE)
    package_price = models.IntegerField(default=0)
    my_offer = models.IntegerField(default=0)
    from_destination = models.TextField()
    to_destination = models.TextField()

    travel_date = models.DateTimeField()
    travel_date_end = models.DateTimeField(default=None, null=True, blank=True)

    pick_up_location = models.TextField(default=None, null=True, blank=True)

    date_recorded = models.DateTimeField(default=datetime.now())
    is_confirmed = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'RENT ID {self.rent_id} || IS DONE : {self.is_done} || IS CONFIRMED : {self.is_confirmed} || IS REJECTED : {self.is_rejected}'
    

class CarpoolVan(models.Model):
    carpool_id = models.CharField(max_length=30)
    available_seat = models.IntegerField(default=0)
    from_destination = models.TextField()
    to_destination = models.TextField()
    plate_no = models.ForeignKey(Van, on_delete=models.CASCADE)
    driver_id = models.ForeignKey(DriverAccount, on_delete=models.CASCADE)
    date_recorded = models.DateTimeField(default=datetime.now())
    is_done = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f'PLATE NO : {self.plate_no.plate_no} || IS DONE : {self.is_done} || IS CANCELLED : {self.is_cancelled}'

class BookedPassenger(models.Model):
    booked_id = models.CharField(max_length=30)
    passenger_id = models.ForeignKey(PassengerAccount, on_delete=models.CASCADE, null=True, blank=True)
    carpool_id = models.ForeignKey(CarpoolVan, on_delete=models.CASCADE)
    fare = models.IntegerField(default=0)
    pick_up_location = models.TextField()
    seats_occupied = models.IntegerField(default=0)
    date_recorded = models.DateTimeField(default=datetime.now())

    is_confirmed = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_dropped = models.BooleanField(default=False)

    date_confirmed = models.DateTimeField(default=None, null=True, blank=True)
    date_rejected = models.DateTimeField(default=None, null=True, blank=True)
    date_cancelled = models.DateTimeField(default=None, null=True, blank=True)
    date_dropped = models.DateTimeField(default=None, null=True, blank=True)

    destination = models.TextField()

    def __str__(self):
        if not self.passenger_id is None:
            return f'PASSENGER : {self.passenger_id.user_id.first_name} {self.passenger_id.user_id.last_name} || DESTINATION : {self.destination} || IS DROPPED : {self.is_dropped} || IS REJECTED : {self.is_rejected} || IS CANCELLED : {self.is_cancelled}'
        else:
            return f'DESTINATION : {self.destination} || IS DROPPED : {self.is_dropped} || IS REJECTED : {self.is_rejected} || IS CANCELLED : {self.is_cancelled}'

    

class Review(models.Model):
    rent_id = models.ForeignKey(RentedVan, on_delete=models.CASCADE, null=True, blank=True)
    carpool_id = models.ForeignKey(BookedPassenger, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    date_recorded = models.DateTimeField(default=datetime.now())
    review_id = models.CharField(max_length=30)

    def __str__(self):
        return f'REVIEW ID : {self.review_id} || RATING : {self.rating}'



class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    date_sent = models.DateTimeField(default=datetime.now())
    date_seen = models.DateTimeField(default=datetime.now())
    is_seen = models.BooleanField(default=False)
    message = models.TextField()
    message_id = models.CharField(max_length=50)

    offer = models.IntegerField(null=True, blank=True, default=0)
    rental_attachment = models.ForeignKey(RentedVan, on_delete=models.CASCADE, null=True, blank=True)
    carpooling_attachment = models.ForeignKey(CarpoolVan, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'SENDER : {self.sender.username} || MESSAGE : {self.message}'
    

class ListOfMunicipalities(models.Model):
    municipality_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.municipality_name}'


class ListOfDestinations(models.Model):
    municipality = models.ForeignKey(ListOfMunicipalities, on_delete=models.CASCADE)
    destination_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.destination_name}'
    

class FAQs(models.Model):
    question = models.TextField()
    answer = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'QUESTION : {self.question} || IS ACTIVE : {self.is_active}'
    
class GetInTouch(models.Model):
    office_address = models.TextField()
    contact_no = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    
    def __str__(self):
        return f'OFFICE ADDRESS {self.office_address}'
    

class TourGallery(models.Model):
    tour_gallery_id = models.CharField(max_length=50, default=None, null=True, blank=True)
    rented_van = models.ForeignKey(RentedVan, on_delete=models.CASCADE)
    description = models.TextField(default=None, null=True, blank=True)
    title = models.TextField(default=None, null=True, blank=True)
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f'TITLE : {self.title} || IS ENABLED : {self.is_enabled}'
    
class TourGalleryImages(models.Model):
    tour_gallery = models.ForeignKey(TourGallery, on_delete=models.CASCADE)
    image = models.TextField()
    is_enabled = models.BooleanField(default = True)

    def __str__(self):
        return f'ID : {self.id} || IS ENABLED : {self.is_enabled}'

    