from django.urls import path

from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.BookingListView.as_view(), name='home'),

    path('bookings/create/', views.BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/cancel/', views.BookingCancelView.as_view(), name='booking-cancel'),

    path('facilities/', views.FacilityListView.as_view(), name='facility-list'),

]
