import uuid
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.utils import json
from rest_framework.views import APIView
import logging

from .constants import PaymentStatus
from .models import Order

logger = logging.getLogger(__name__)


def make_payment(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))  # Convert amount to paise
        client = razorpay.Client(auth=('rzp_test_F2b1KRv9bcdtMC', 'C6c2P8UoajS6JaWSt2sValks'))
        payment = client.order.create({
            'amount': amount,
            'currency': 'INR',
            'payment_capture': '1'
        })

        context = {
            'razorpay_key': 'rzp_test_F2b1KRv9bcdtMC',
            'order_id': payment['id'],
            'amount': 100.00
        }
        return render(request, 'payment.html', context)
    return render(request, 'payment_form.html')


# def is_admin(user):
# return user.is_authenticated and user.is_staff

# @user_passes_test(is_admin)
def payment_success(request, pay_id, order_id):
    try:
        # Simulate retrieval of payment details
        payment = {
            'pay_id': pay_id,
            'order_id': order_id,
            'status': 'success',
        }
        return render(request, 'payment_success.html', payment)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


class PaymentDetailsView(APIView):
    def get(self, request, pay_id, order_id):
        # Simulate retrieval of payment details
        payment_data = {
            'pay_id': pay_id,
            'order_id': order_id,
            'status': 'success',
            'amount': 100.00,  # Example amount in INR
        }

        # Initialize Razorpay client with your API key and secret
        client = razorpay.Client(auth=('rzp_test_F2b1KRv9bcdtMC', 'C6c2P8UoajS6JaWSt2sValks'))

        try:
            # Convert amount to paise and ensure it meets the minimum requirement
            order_amount = int(payment_data['amount'] * 100)  # Convert amount to paise
            if order_amount < 100:
                raise ValueError("Order amount must be at least ₹1.00")

            # Generate an order with Razorpay
            order_currency = 'INR'  # Change this if your currency is different
            order_receipt = f'order_rcptid_{order_id}'  # Generate a unique order receipt ID

            razorpay_order = client.order.create(
                {
                    'amount': order_amount,
                    'currency': order_currency,
                    'receipt': order_receipt,
                }
            )

            # Pass necessary data to the payment details template
            payment_data['razorpay_order_id'] = razorpay_order['id']
            payment_data['razorpay_amount'] = order_amount
            payment_data['razorpay_currency'] = order_currency
            payment_data['razorpay_key'] = 'rzp_test_F2b1KRv9bcdtMC'  # Add your Razorpay key ID here

            return render(request, 'payment_details.html', payment_data)

        except (razorpay.errors.BadRequestError, ValueError) as e:
            logger.error(f"Error creating Razorpay order: {e}")
            return render(request, 'payment_failed.html', {'errors': str(e)})


def order_payment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=razorpay_order["id"]
        )
        order.save()
        return render(
            request,
            "demo_payment.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
                "razorpay_key": 'rzp_test_F2b1KRv9bcdtMC',
                "order": order,
            },
        )
    return render(request, "demo_payment.html")


@csrf_exempt
def razorpay_callback(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')

            logger.info(
                f"Received Razorpay callback: payment_id={payment_id}, order_id={order_id}, signature={signature}")

            if not payment_id or not order_id or not signature:
                raise ValueError("Missing required Razorpay payment data")

            # Verify the signature
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            try:
                client.utility.verify_payment_signature(params_dict)
                logger.info("Signature verification successful")
            except razorpay.errors.SignatureVerificationError as e:
                logger.error(f"Signature verification failed: {e}")
                return render(request, 'callback.html', {'status': 'failed', 'error': 'Signature verification failed'})

            # Update order status to 'paid'
            try:
                order = Order.objects.get(provider_order_id=order_id)
                order.status = 'paid'
                order.save()
                logger.info(f"Order {order_id} updated to paid")
                return render(request, 'callback.html', {'status': 'success', 'payment_id': payment_id})
            except ValueError as ve:
                logger.error(f"ValueError: {ve}")
                return render(request, 'callback.html', {'status': 'failed', 'error': str(ve)})
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return render(request, 'callback.html', {'status': 'failed', 'error': 'An unexpected error occurred'})

    return render(request, 'callback.html', {'status': 'failed', 'error': 'Invalid request method'})


class GeneratePaymentDetailsView(APIView):
    def get(self, request):
        # Generate mock pay_id and order_id
        pay_id = str(uuid.uuid4())
        order_id = str(uuid.uuid4())
        # Redirect to the existing payment details endpoint
        return redirect('payment_success', pay_id=pay_id, order_id=order_id)


class PaymentSuccessView(APIView):
    def post(self, request):
        try:
            # Razorpay signature verification
            client = razorpay.Client(auth=('rzp_test_F2b1KRv9bcdtMC', 'C6c2P8UoajS6JaWSt2sValks'))
            data = request.data

            # Extract the required parameters from the request
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_signature = data.get('razorpay_signature')

            # Verify the payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            client.utility.verify_payment_signature(params_dict)

            # Handle the success case (e.g., update your order status in the database)
            return JsonResponse({'status': 'Payment successful'})
        except razorpay.errors.SignatureVerificationError as e:
            logger.error(f"Razorpay signature verification failed: {e}")
            return JsonResponse({'error': 'Razorpay signature verification failed'}, status=400)
