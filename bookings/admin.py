from django.contrib import admin

from .models import Facility, Booking


class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity')
    search_fields = ['name']


class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'facility', 'date', 'start_time', 'end_time', 'status')
    search_fields = ['user__username', 'facility__name']
    list_filter = ['facility', 'date', 'status']


admin.site.register(Facility, FacilityAdmin)
admin.site.register(Booking, BookingAdmin)
