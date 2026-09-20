from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Vehicle(models.Model):
    TYPE_CHOICES = [
        ('Hatchback', 'Hatchback'),
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV / Compact SUV'),
        ('Luxury', 'Premium / Luxury'),
        ('EV', 'Electric Vehicle (EV)'),
        ('Coupe', 'Coupe / Sports'),
        ('Truck', 'Truck / Pickup'),
        ('Convertible', 'Convertible'),
        ('Wagon', 'Wagon / Estate'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending Sale'),
        ('sold', 'Sold'),
    ]

    FUEL_CHOICES = [
        ('Gasoline', 'Petrol / Gasoline'),
        ('Diesel', 'Diesel (CRDi/TDI)'),
        ('Electric', 'Electric (BEV)'),
        ('Hybrid', 'Strong Hybrid / Mild Hybrid'),
        ('CNG', 'Bi-Fuel CNG'),
    ]

    TRANSMISSION_CHOICES = [
        ('Automatic', 'Automatic (Torque Converter / CVT)'),
        ('Manual', 'Manual (5-Speed / 6-Speed)'),
        ('Dual-Clutch', 'Dual-Clutch (DCT / DSG)'),
        ('Single-Speed', 'Single-Speed (EV Direct Drive)'),
    ]

    DRIVETRAIN_CHOICES = [
        ('FWD', 'Front-Wheel Drive (FWD)'),
        ('RWD', 'Rear-Wheel Drive (RWD)'),
        ('AWD', 'All-Wheel Drive (AWD)'),
        ('4WD', 'Four-Wheel Drive (4x4)'),
    ]

    # Core identification
    vin = models.CharField('VIN Number', max_length=17, unique=True, db_index=True)
    year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2030)]
    )
    make = models.CharField(max_length=64, db_index=True)
    model = models.CharField(max_length=64, db_index=True)
    trim = models.CharField(max_length=64, blank=True, help_text='e.g. Alpha, ZX, AX7 L, M Sport, SX(O)')

    # Specifications
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Sedan')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', db_index=True)
    odometer = models.PositiveIntegerField('Odometer (km)', default=0, help_text='Odometer reading in kilometers')
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text='Ex-showroom / sale price in INR (₹)')
    
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='Gasoline')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='Automatic')
    drivetrain = models.CharField(max_length=20, choices=DRIVETRAIN_CHOICES, default='FWD')
    
    exterior_color = models.CharField(max_length=100, blank=True, default='Pearl Arctic White')
    interior_color = models.CharField(max_length=100, blank=True, default='Dual-Tone Ebony & Ivory Leatherette')
    engine = models.CharField(max_length=100, blank=True, default='1.5L Turbocharged Petrol')
    horsepower = models.PositiveIntegerField(null=True, blank=True, help_text='Brake Horsepower (BHP / PS)')

    # Visuals & Content
    primary_image_url = models.URLField(
        max_length=500,
        blank=True, 
        default='', 
        help_text='Direct URL for high-res vehicle photo (e.g. Unsplash automotive CDN)'
    )
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    description = models.TextField(blank=True)
    features = models.TextField(
        blank=True, 
        help_text='Comma-separated highlights (e.g. Sport Chrono, Carbon Ceramic Brakes, Apple CarPlay)'
    )
    featured = models.BooleanField(default=False, help_text='Show in Showroom Highlights')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'

    def __str__(self):
        trim_str = f" {self.trim}" if self.trim else ""
        return f"{self.year} {self.make} {self.model}{trim_str} ({self.vin})"

    def get_absolute_url(self):
        return reverse('inventory:vehicle_detail', kwargs={'pk': self.pk})

    @property
    def title(self):
        trim_str = f" {self.trim}" if self.trim else ""
        return f"{self.year} {self.make} {self.model}{trim_str}"

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.primary_image_url:
            return self.primary_image_url
        return 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1000&q=80'

    @property
    def feature_list(self):
        if not self.features:
            return []
        return [f.strip() for f in self.features.split(',') if f.strip()]

    @property
    def status_badge_class(self):
        mapping = {
            'available': 'badge-status-available',
            'pending': 'badge-status-pending',
            'sold': 'badge-status-sold',
        }
        return mapping.get(self.status, 'badge-status-available')


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='gallery_images')
    image_url = models.URLField(max_length=500, blank=True, default='')
    image = models.ImageField(upload_to='vehicles/gallery/', blank=True, null=True)
    caption = models.CharField(max_length=120, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'Vehicle Gallery Image'
        verbose_name_plural = 'Vehicle Gallery Images'

    def __str__(self):
        return f"Image for {self.vehicle.title} ({self.caption or 'Untitled'})"

    @property
    def display_url(self):
        if self.image:
            return self.image.url
        return self.image_url
