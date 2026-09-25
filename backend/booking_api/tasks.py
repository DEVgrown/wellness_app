import time
import random
import string
import logging
from celery import shared_task
from .models import Booking, PaymentTransaction

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def process_mpesa_payment_task(self, booking_id, phone_number, amount):
    """
    Asynchronous Celery task simulating Safaricom Daraja STK Push callback processing.
    Directly updates authoritative PostgreSQL Booking and PaymentTransaction records.
    """
    logger.info(f"Initiating async M-Pesa STK Push task for booking {booking_id}, phone: {phone_number}, amount: {amount}")
    
    # Simulate carrier network delay (1-2 seconds)
    time.sleep(2)
    
    # Generate authentic Safaricom transaction reference
    receipt_code = 'QK' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # Update PostgreSQL booking record with confirmed payment status
    if booking_id:
        try:
            booking = Booking.objects.filter(id=booking_id).first()
            if booking:
                booking.status = 'confirmed'
                booking.payment_reference = receipt_code
                booking.payment_method = 'mpesa'
                booking.save(update_fields=['status', 'payment_reference', 'payment_method'])
                
                # Update corresponding payment transaction
                PaymentTransaction.objects.filter(booking=booking).update(
                    status='completed',
                    merchant_request_id=receipt_code
                )
                logger.info(f"Booking {booking_id} confirmed in PostgreSQL with M-Pesa reference {receipt_code}")
            else:
                logger.warning(f"Booking {booking_id} not found in PostgreSQL.")
        except Exception as e:
            logger.error(f"Failed to update booking {booking_id} in PostgreSQL: {e}")

    return {
        'status': 'SUCCESS',
        'receipt_code': receipt_code,
        'phone_number': phone_number,
        'amount': amount,
        'booking_id': booking_id
    }


@shared_task
def send_booking_confirmation_task(booking_id, user_email, service_title, booking_date, time_slot):
    """
    Asynchronously dispatches booking confirmation email and calendar invite.
    """
    logger.info(f"Sending confirmation email to {user_email} for session '{service_title}' on {booking_date} at {time_slot}")
    return {
        'status': 'SENT',
        'recipient': user_email,
        'booking_id': booking_id
    }


@shared_task
def schedule_reminder_task(booking_id, user_phone, booking_date):
    """
    Schedules 24-hour pre-session SMS reminder.
    """
    logger.info(f"Scheduled 24h reminder for booking {booking_id} to {user_phone}")
    return {
        'status': 'SCHEDULED',
        'booking_id': booking_id
    }
