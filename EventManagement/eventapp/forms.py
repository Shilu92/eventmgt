from django import forms
from .models import Event, VenueBooking, Ticket, Registration, Attendee


class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'image', 'event_date']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(EventModelForm, self).__init__(*args, **kwargs)
        # Set the input type for the 'image' field to 'file'
        self.fields['image'].widget.attrs['type'] = 'file'
        self.fields['event_date'].widget.attrs.update({'class': 'datetimepicker'})


class VenueBookingForm(forms.ModelForm):
    class Meta:
        model = VenueBooking
        fields = ['venue', 'date', 'time', 'additional_info']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(VenueBookingForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'class': 'datetimepicker'})


class TicketPurchaseForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event', 'name', 'price', 'quantity_available']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'] = forms.DecimalField(label='Price', disabled=False)
        self.fields['quantity_available'] = forms.IntegerField(label='Available Quantity', disabled=False)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['event', 'user', 'additional_details']


class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['name', 'email', 'event', 'location']
