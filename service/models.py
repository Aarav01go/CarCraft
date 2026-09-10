from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone


class ServiceBay(models.Model):
    name = models.CharField(max_length=64, unique=True, help_text='e.g. Bay 1 - Dyno & Diagnostics')
    bay_number = models.PositiveSmallIntegerField(unique=True)
    assigned_technician = models.CharField(max_length=100, help_text='Lead Technician / ASE Certified Specialist')
    specialty = models.CharField(max_length=100, default='General Automotive Service')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['bay_number']
        verbose_name = 'Service Bay'
        verbose_name_plural = 'Service Bays'

    def __str__(self):
        return f"Bay #{self.bay_number}: {self.name} ({self.assigned_technician})"


class Appointment(models.Model):
    SERVICE_TYPES = [
        ('oil_synthetic', 'Full Synthetic Oil & Filter Service (₹4,500)'),
        ('brake_performance', 'Performance Brake Pad & Rotor Service (₹12,500)'),
        ('tire_alignment', 'Tire Rotation, Laser Balancing & 4-Wheel Alignment (₹3,200)'),
        ('diagnostics_full', 'Comprehensive OBD-II Computer & Electrical Diagnostics (₹2,800)'),
        ('multi_point_inspection', '50-Point Certified Pre-Purchase / Safety Inspection (₹2,500)'),
        ('transmission_flush', 'Transmission Flush & Drivetrain Fluid Service (₹8,900)'),
        ('ev_battery_health', 'EV / Hybrid High-Voltage Battery Health & Cooling Diagnostic (₹4,200)'),
        ('performance_tune', 'Custom ECU Stage-1 Calibration & Dyno Optimization (₹18,500)'),
    ]

    TIME_SLOTS = [
        ('08:00', '08:00 AM - 09:30 AM'),
        ('09:30', '09:30 AM - 11:00 AM'),
        ('11:00', '11:00 AM - 12:30 PM'),
        ('13:00', '01:00 PM - 02:30 PM'),
        ('14:30', '02:30 PM - 04:00 PM'),
        ('16:00', '04:00 PM - 05:30 PM'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress / On Lift'),
        ('completed', 'Completed / Ready for Pickup'),
        ('cancelled', 'Cancelled'),
    ]

    SERVICE_COSTS = {
        'oil_synthetic': 4500.00,
        'brake_performance': 12500.00,
        'tire_alignment': 3200.00,
        'diagnostics_full': 2800.00,
        'multi_point_inspection': 2500.00,
        'transmission_flush': 8900.00,
        'ev_battery_health': 4200.00,
        'performance_tune': 18500.00,
    }

    # Customer Information
    customer_name = models.CharField('Customer Full Name', max_length=100)
    customer_email = models.EmailField('Email Address')
    customer_phone = models.CharField('Phone Number', max_length=25)

    # Vehicle Information
    vehicle_description = models.CharField(
        'Vehicle Year, Make & Model', 
        max_length=150, 
        help_text='e.g. 2024 Mahindra XUV700 AX7L / 2024 Hyundai Ioniq 5'
    )
    vehicle_vin = models.CharField('VIN (Optional)', max_length=17, blank=True)
    vehicle_odometer = models.PositiveIntegerField('Current Odometer (km)', null=True, blank=True)

    # Scheduling
    service_type = models.CharField(max_length=40, choices=SERVICE_TYPES, default='oil_synthetic')
    date = models.DateField(db_index=True)
    time_slot = models.CharField(max_length=10, choices=TIME_SLOTS, default='08:00', db_index=True)
    
    assigned_bay = models.ForeignKey(
        ServiceBay, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='appointments'
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', db_index=True)
    notes = models.TextField('Customer Notes / Specific Concerns', blank=True)
    internal_notes = models.TextField('Technician Workshop Notes', blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'time_slot', 'assigned_bay__bay_number']
        verbose_name = 'Service Appointment'
        verbose_name_plural = 'Service Appointments'

    def __str__(self):
        return f"{self.date} {self.time_slot} - {self.customer_name} ({self.get_service_type_display().split('(')[0].strip()})"

    @property
    def vehicle_mileage(self):
        return self.vehicle_odometer

    @vehicle_mileage.setter
    def vehicle_mileage(self, value):
        self.vehicle_odometer = value

    def clean(self):
        super().clean()
        if self.assigned_bay and self.date and self.time_slot and self.status != 'cancelled':
            conflicts = Appointment.objects.filter(
                assigned_bay=self.assigned_bay,
                date=self.date,
                time_slot=self.time_slot
            ).exclude(status='cancelled').exclude(pk=self.pk)
            
            if conflicts.exists():
                raise ValidationError(
                    f"{self.assigned_bay.name} is already booked on {self.date} during {self.get_time_slot_display()}."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.estimated_cost or self.estimated_cost == 0:
            self.estimated_cost = self.SERVICE_COSTS.get(self.service_type, 4500.00)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service:appointment_detail', kwargs={'pk': self.pk})

    @property
    def status_ticket_class(self):
        mapping = {
            'scheduled': 'ticket-scheduled',
            'in_progress': 'ticket-in-progress',
            'completed': 'ticket-completed',
            'cancelled': 'ticket-cancelled',
        }
        return mapping.get(self.status, 'ticket-scheduled')

    @property
    def service_label_short(self):
        return self.get_service_type_display().split('(')[0].strip()
