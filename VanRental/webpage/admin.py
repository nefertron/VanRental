from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(AdminAccount)
admin.site.register(DriverAccount)
admin.site.register(PassengerAccount)
admin.site.register(Notification)
admin.site.register(Van)
admin.site.register(RentedVan)
admin.site.register(CarpoolVan)
admin.site.register(BookedPassenger)
admin.site.register(Review)
admin.site.register(Messages)
admin.site.register(ListOfMunicipalities)
admin.site.register(ListOfDestinations)