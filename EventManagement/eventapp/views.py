from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import EventModelForm, VenueBookingForm, TicketPurchaseForm, RegistrationForm, AttendeeForm
from .models import Event, Venue, VenueBooking, Ticket, Attendee


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event successfully registered")
            return redirect('event_list')
        else:
            # Handle invalid form
            messages.error(request, "Failed to register event. Please check your input.")
            return redirect('event_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    events = Event.objects.all()
    print(events)
    return render(request, 'index.html', {'events': events})


def about(request):
    events = Event.objects.all()
    return render(request, 'about.html', {'events': events})


def contact_us(request):
    events = Event.objects.all()
    return render(request, 'contact_us.html', {'events': events})


def terms(request):
    events = Event.objects.all()
    return render(request, 'terms.html', {'events': events})


def privacy(request):
    events = Event.objects.all()
    return render(request, 'privacy.html', {'events': events})


def admin_page(request):
    events = Event.objects.all()
    return render(request, 'home.html', {'events': events})


def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})


def event_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('create_event')
        else:
            error_message = "Invalid username or password"
    else:
        error_message = None

    return render(request, 'event_login.html', {'error_message': error_message})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('event_list')

    form = EventModelForm()
    return render(request, 'create_event.html', {'form': form})


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event_detail.html', {'event': event})


def venue_list(request):
    venue = Venue.objects.all()
    return render(request, 'venue_list.html', {'venue': venue})


def venue_booking(request):
    if request.method == 'POST':
        form = VenueBookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_success')  # Redirect to a success page

    form = VenueBookingForm()
    return render(request, 'venue_booking.html', {'form': form})


def booking_success(request):
    return render(request, 'booking_success.html')


def booking_details(request, booking_id):
    booking = get_object_or_404(VenueBooking, pk=booking_id)
    return render(request, 'booking_details.html', {'booking': booking})


def venue_booking_list(request):
    bookings = VenueBooking.objects.all()
    return render(request, 'venue_booking_list.html', {'bookings': bookings})


def venue_details(request):
    venue = Venue.objects.all()
    return render(request, 'venue_details.html', {'venue': venue})


def register_for_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.save()
            return redirect('registration_success')
    else:
        form = RegistrationForm()
    return render(request, 'register_attendee.html', {'form': form, 'event': event})


def registration_success(request):
    return render(request, 'registration_success.html')


def attendee_list(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    attendees = Attendee.objects.filter(event=event)
    context = {
        'event': event,
        'attendees': attendees,
    }
    return render(request, 'attendee_list.html', context)


def event_attendee_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    attendees = Attendee.objects.filter(event=event)
    return render(request, 'event_attendee_detail.html', {'event': event, 'attendees': attendees})


def register_attendee(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save(commit=False)
            attendee.event = event
            attendee.save()
            return redirect('event_attendee_detail', event_id=event.id)
    else:
        form = AttendeeForm()
    return render(request, 'attendee_form.html', {'form': form, 'event': event})


def check_in_attendee(request, attendee_id):
    attendee = get_object_or_404(Attendee, pk=attendee_id)
    attendee.check_in_time = timezone.now()
    attendee.save()
    return redirect('event_attendee_detail', event_id=attendee.event.id)


def select_ticket(request):
    return render(request, 'ticket_selection.html')


def ticket_purchase(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    tickets = Ticket.objects.filter(event=event, quantity_available__gt=0)

    if request.method == 'POST':
        form = TicketPurchaseForm(request.POST)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.event = event  # Associate the ticket with the event
            new_ticket.save()
            return redirect('confirmation', event_id=event.id)
    else:
        form = TicketPurchaseForm()
        return render(request, 'ticket_purchase.html', {'event': event, 'tickets': tickets, 'form': form})


def confirmation(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'confirmation.html', {'event': event})


def ticket_purchase_details(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    tickets = Ticket.objects.filter(event=event)
    return render(request, 'ticket_purchase_details.html', {'event': event, 'tickets': tickets})


def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def send_event_invitation(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        email = request.POST.get('email')
        message = f"You're invited to attend {event.title} on {event.event_date}."
        send_mail('Event Invitation', message, 'fdxxdf46@gmail.com', [email])
        return redirect('event_list')
    return render(request, 'send_invitation.html', {'event': event})


def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def admin_page(request):
    return render(request, 'home.html')


def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


def send_email(request):
    if request.method == 'POST':
        to_email = request.POST.get('email')
        subject = 'Event Promotion'
        message = 'Hi'
        from_email = 'fdxxdf46@gmail.com'  # Sender's email address
        send_mail(subject, message, from_email, [to_email])
        return HttpResponse('Email sent successfully!')
    return render(request, 'send_email.html')


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'DELETE':
        event.delete()
        return JsonResponse({'message': 'Event deleted successfully'}, status=200)
    elif request.method == 'GET':
        return render(request, 'delete_event.html', {'event': event})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
