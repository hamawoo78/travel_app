from django.contrib import admin

# Register your models here.
from .models import Address, Hotel, Plan

admin.site.register(Address)
admin.site.register(Hotel)
admin.site.register(Plan)
