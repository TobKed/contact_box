from django.contrib import admin
from .models import Person, Address, PhoneNumber, Email, ContactGroup, Profile

admin.site.register(Person)
admin.site.register(Address)
admin.site.register(PhoneNumber)
admin.site.register(Email)
admin.site.register(ContactGroup)
admin.site.register(Profile)
