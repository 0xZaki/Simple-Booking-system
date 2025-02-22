from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView

from .forms import BookingForm
from .models import Booking, Facility


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
        return Booking.objects.filter(user=self.request.user)


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
        messages.success(self.request, 'Booking created successfully!')
        return super().form_valid(form)


class BookingCancelView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=kwargs["pk"], user=request.user)
        booking.status = "canceled"
        booking.save()
        messages.success(request, "Booking has been canceled!")
        return HttpResponseRedirect(reverse_lazy("bookings:home"))
