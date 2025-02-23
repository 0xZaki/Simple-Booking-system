from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Booking, Facility

User = get_user_model()


# Test Booking Views
class BookingListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.client.force_login(self.user)
        Facility.objects.create(name='Test Facility', location='Test Location', capacity=10)
        Booking.objects.create(
            user=self.user,
            date='2023-01-01',
            start_time='10:00',
            end_time='11:00',
            status='confirmed',
            facility=Facility.objects.first()
        )

    def test_view_url(self):
        response = self.client.get(reverse('bookings:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_list.html')
        bookings = response.context['bookings']
        self.assertEqual(len(bookings), 1)

    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('bookings:home'))
        self.assertEqual(response.status_code, 302)


class BookingCancelViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', email='test1@test.com'
        )
        self.client.force_login(self.user)
        Facility.objects.create(name='Test Facility', location='Test Location', capacity=10)
        self.booking = Booking.objects.create(
            user=self.user,
            date='2023-01-01',
            start_time='10:00',
            end_time='11:00',
            status='confirmed',
            facility=Facility.objects.first()
        )

    def test_view_url(self):
        response = self.client.post(reverse('bookings:booking-cancel', args=[self.booking.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.get(pk=self.booking.pk).status, 'canceled')

    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse('bookings:booking-cancel', args=[self.booking.pk]))
        self.assertEqual(response.status_code, 302)

    def test_cancel_another_users_booking(self):
        another_user = User.objects.create_user(
            username='anotheruser', password='testpassword', email='test2@test.com'
        )
        self.client.force_login(another_user)
        response = self.client.post(reverse('bookings:booking-cancel', args=[self.booking.pk]))
        self.assertEqual(response.status_code, 404)


class BookingCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', email='test1@test.com'
        )
        self.client.force_login(self.user)
        self.facility = Facility.objects.create(name='Test Facility', location='Test Location', capacity=1)

    def test_view_url(self):
        response = self.client.get(reverse('bookings:booking-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_form.html')

    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('bookings:booking-create'))
        self.assertEqual(response.status_code, 302)

    def test_create_booking(self):
        form_data = {
            'date': '2025-02-24',
            'start_time': '10:00',
            'end_time': '11:00',
            'facility': self.facility.pk
        }
        response = self.client.post(reverse('bookings:booking-create'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.first().user, self.user)

    def test_create_invalid_old_date_booking(self):
        form_data = {
            'date': '2022-02-24',
            'start_time': '10:00',
            'end_time': '11:00',
            'facility': self.facility.pk
        }
        response = self.client.post(reverse('bookings:booking-create'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_form.html')
        self.assertIn('start_time', response.context['form'].errors)

    def test_create_invalid_end_date_booking(self):
        form_data = {
            'date': '2025-02-24',
            'start_time': '11:00',
            'end_time': '10:00',
            'facility': self.facility.pk,
        }
        response = self.client.post(reverse('bookings:booking-create'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_form.html')
        self.assertIn('end_time', response.context['form'].errors)

    def test_fully_booked_facility(self):
        form_data = {
            'date': '2025-02-24',
            'start_time': '10:00',
            'end_time': '11:00',
            'facility': self.facility.pk
        }
        Booking.objects.create(
            user=self.user,
            date='2025-02-24',
            start_time='10:30',
            end_time='11:00',
            status='confirmed',
            facility=self.facility
        )
        response = self.client.post(reverse('bookings:booking-create'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_form.html')
        self.assertIn('facility', response.context['form'].errors)


# test facility view
class FacilityListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', email='test1@test.com'
        )
        self.client.force_login(self.user)
        Facility.objects.create(name='Test Facility', location='Test Location', capacity=10)

    def test_view_url(self):
        response = self.client.get(reverse('bookings:facility-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/facility_list.html')
        facilities = response.context['facilities']
        self.assertEqual(len(facilities), 1)

    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('bookings:facility-list'))
        self.assertEqual(response.status_code, 302)
