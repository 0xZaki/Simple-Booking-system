import logging
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView

from .forms import BookingForm
from .models import Booking, Facility
from .tasks import send_confirmation_email, send_cancellation_email


# Facility Views
class FacilityListView(LoginRequiredMixin, ListView):
    model = Facility
    context_object_name = 'facilities'

    template_name = 'bookings/facility_list.html'


# Booking Views
class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    context_object_name = 'bookings'
    template_name = 'bookings/booking_list.html'
    ordering = ['-date', '-start_time']

    def get_queryset(self):
        booking = Booking.objects.filter(user=self.request.user)
        for b in booking:
            if b.status == 'confirmed' and datetime.combine(b.date, b.start_time) >= datetime.now():
                b.cancellable = True
            else:
                b.cancellable = False
        return booking


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('bookings:home')

    def get_initial(self):
        initial = super().get_initial()
        facility_id = self.request.GET.get('facility')
        if facility_id:
            initial['facility'] = facility_id
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        booking = super().form_valid(form)
        send_confirmation_email.delay(form.instance.pk)
        logging.info(f"Booking created successfully with ID: {form.instance.pk}")
        messages.success(self.request, 'Booking created successfully! Email with booking details will be sent.')
        return booking


class BookingCancelView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=kwargs["pk"], user=request.user)
        if booking.status != "confirmed":
            messages.error(request, "You can only cancel confirmed bookings.")
            return HttpResponseRedirect(reverse_lazy("bookings:home"))
        elif datetime.combine(booking.date, booking.start_time) < datetime.now():
            messages.error(request, "You can only cancel bookings that have not started yet.")
        else:
            booking.status = "canceled"
            send_cancellation_email.delay(booking.pk)
            booking.save()
            logging.info(f"Booking canceled successfully with ID:{booking.pk}")
            messages.success(request, "Booking has been canceled!")
        return HttpResponseRedirect(reverse_lazy("bookings:home"))
