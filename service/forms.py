from django import forms
from django.utils import timezone
from .models import Appointment
from .services import get_active_bays, get_available_bays


class AppointmentBookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'customer_name', 'customer_email', 'customer_phone',
            'vehicle_description', 'vehicle_vin', 'vehicle_odometer',
            'service_type', 'date', 'time_slot', 'notes'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Rahul Sharma'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'rahul.sharma@example.in'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 98201 23456'}),
            'vehicle_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2024 Mahindra XUV700 AX7L'}),
            'vehicle_vin': forms.TextInput(attrs={'class': 'form-control font-monospace text-uppercase', 'placeholder': '17-digit VIN (Optional)', 'maxlength': '17'}),
            'vehicle_odometer': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 12500'}),
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time_slot': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe symptoms, periodic service requests, or custom performance requirements...'}),
        }

    def clean_date(self):
        booking_date = self.cleaned_data.get('date')
        if booking_date and booking_date < timezone.now().date():
            raise forms.ValidationError("Appointments cannot be booked for past dates. Please select today or a future date.")
        return booking_date

    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('date')
        time_slot = cleaned_data.get('time_slot')

        if booking_date and time_slot:
            active_bays = get_active_bays()
            if not active_bays.exists():
                raise forms.ValidationError("No service bays are currently active. Please contact the service desk directly.")

            available_bays = get_available_bays(booking_date, time_slot)
            if not available_bays.exists():
                raise forms.ValidationError(
                    f"⚠️ Workshop Bay Capacity Reached: All {active_bays.count()} service bays are fully booked for "
                    f"{booking_date.strftime('%B %d, %Y')} at {dict(Appointment.TIME_SLOTS).get(time_slot)}. "
                    f"Please select an alternate time slot or date."
                )

            # Auto-assign the first available bay
            self.auto_assigned_bay = available_bays.first()

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if hasattr(self, 'auto_assigned_bay') and self.auto_assigned_bay:
            instance.assigned_bay = self.auto_assigned_bay
        if commit:
            instance.save()
        return instance


class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status', 'assigned_bay', 'internal_notes', 'estimated_cost']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_bay': forms.Select(attrs={'class': 'form-select'}),
            'internal_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Technician diagnostics log, lift observations, torque check completed...'}),
            'estimated_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
