from django.contrib import admin
from django.urls import path

from . import views
from .views import PaymentDetailsView, GeneratePaymentDetailsView, PaymentSuccessView

urlpatterns = [
    path("payment/", views.order_payment, name="payment"),
    path('payment_success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('payment_success/', GeneratePaymentDetailsView.as_view(), name='payment_success'),
    path("razorpay/callback/", views.razorpay_callback, name="razorpay_callback"),
    #path('payment_success/', PaymentSuccessView.as_view(), name='payment_success'),
    #path('make_payment/', views.make_payment, name='make_payment'),
    #path('payment_details/generate/', GeneratePaymentDetailsView.as_view(), name='generate_payment_details'),
    #path('make_payment/payment_success/', PaymentSuccessView.as_view(), name='payment_success'),
    #path('payment_details/<str:pay_id>/<str:order_id>/success/', PaymentDetailsView.as_view(), name='payment_details'),
    ]
