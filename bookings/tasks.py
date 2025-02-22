import logging

from django.core.mail import send_mail

from config import celery_app
from .models import Booking


@celery_app.task
def send_confirmation_email(booking_id):
    logging.info(f"send_confirmation_email called with booking_id: {booking_id}")
    booking = Booking.objects.get(pk=booking_id)
    email = booking.user.email
    if email:
        logging.info(f"Sending email to: {email}")
        send_mail(
            'Booking Confirmation',
            f'Your booking for {booking.facility.name} on {booking.date} has been confirmed.',
            [email],
            recipient_list=[email],
        )


@celery_app.task
def send_cancellation_email(booking_id):
    logging.info(f"send_cancellation_email called with booking_id: {booking_id}")
    booking = Booking.objects.get(pk=booking_id)
    email = booking.user.email
    if email:
        logging.info(f"Sending email to: {email}")
        send_mail(
            'Booking Cancellation',
            f'Your booking for {booking.facility.name} on {booking.date} has been canceled.',
            [email],
            recipient_list=[email],
        )
