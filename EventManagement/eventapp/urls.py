
from django.urls import path
from .import views


urlpatterns = [
    path("", views.signup, name='signup'),
    path("home", views.home, name='home'),
    path("about/", views.about, name='about'),
    path("terms/", views.terms, name='terms'),
    path("contact_us/", views.contact_us, name='contact_us'),
    path("privacy/", views.privacy, name='privacy'),
    path("admin_page", views.admin_page, name='admin_page'),
    path("event_list/", views.event_list, name='event_list'),
    path("event_list/event_login", views.event_login, name='event_list/event_login'),
    path("event_list/create_event/", views.create_event, name='create_event'),
    path("events/<int:event_id>/", views.event_detail, name='event_detail'),
    path('event_attendee_detail/<int:event_id>/', views.event_attendee_detail, name='event_attendee_detail'),
    path('events/<int:event_id>/register/', views.register_attendee, name='register_attendee'),
    path('attendees/<int:attendee_id>/check_in/', views.check_in_attendee, name='check_in_attendee'),
    path('events/<int:event_id>/attendees/', views.attendee_list, name='attendee_list'),
    path('events/<int:event_id>/send-invitation/', views.send_event_invitation, name='send_event_invitation'),
    path("venue_list/", views.venue_list, name='venue_list'),
    path("venue_booking/", views.venue_booking, name='venue_booking'),
    path("booking_success/", views.booking_success, name='booking_success'),
    path('venue_bookings/', views.venue_booking_list, name='venue_booking_list'),
    path('booking_details/<int:booking_id>/', views.booking_details, name='booking_details'),
    path("venue_details/", views.venue_details, name='venue_details'),
    path('events/<int:event_id>/registers/', views.register_for_event, name='register_for_event'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('select_ticket/', views.select_ticket, name='select_ticket'),
    path('ticket_purchase/<int:event_id>/', views.ticket_purchase, name='ticket_purchase'),
    path('ticket_purchase_details', views.ticket_purchase_details, name='ticket_purchase_details'),
    path("confirmation/<int:event_id>/", views.confirmation, name='confirmation'),
    path("attendees/", views.attendee_list, name='attendees'),
    path('users/', views.user_list, name='user_list'),
    path('send_email/', views.send_email, name='send_email'),
    path('events/<int:event_id>/delete_event/', views.delete_event, name='delete_event'),
    path("about/", views.about, name='about'),
    #path("terms/", views.terms, name='terms'),
    #path("contact_us/", views.contact_us, name='contact_us'),
    #path("privacy/", views.privacy, name='privacy'),


]




