import datetime

from django import forms
from django.utils.timezone import now, make_aware

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['facility', 'date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        facility = cleaned_data.get('facility')

        if date and start_time:
            selected_datetime = datetime.datetime.combine(date, start_time)
            selected_datetime = make_aware(selected_datetime)  # Convert to timezone-aware

            if selected_datetime <= now():
                self.add_error('start_time', 'Start time must be in the future.')

        if start_time and end_time and start_time >= end_time:
            self.add_error('end_time', "End time must be after start time.")

        if facility and date and start_time and end_time:
            overlapping_bookings = Booking.objects.filter(
                facility=facility,
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time,
                status='confirmed'
            ).count()

            if overlapping_bookings >= facility.capacity:
                self.add_error('facility', 'This facility is fully booked at the selected time.')

        return cleaned_data
