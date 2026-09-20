import uuid
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    icon = models.CharField(max_length=40, default='bi-gear-wide-connected', help_text='Bootstrap Icon class')
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"{reverse('store:catalog')}?category={self.slug}"


class Part(models.Model):
    sku = models.CharField('SKU / Part Number', max_length=32, unique=True, db_index=True)
    name = models.CharField(max_length=150, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='parts')
    brand = models.CharField(max_length=64, default='CarCraft OEM Performance')
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    stock = models.PositiveIntegerField(default=0)
    
    description = models.TextField(blank=True)
    specifications = models.TextField(
        blank=True, 
        help_text='Fitment, material, dimensions, compatibility guide'
    )
    primary_image_url = models.URLField(max_length=500, blank=True, default='', help_text='High-res photo URL')
    image = models.ImageField(upload_to='parts/', blank=True, null=True)
    
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', 'name']
        verbose_name = 'Part & Accessory'
        verbose_name_plural = 'Parts & Accessories'

    def __str__(self):
        return f"{self.name} [{self.sku}]"

    def get_absolute_url(self):
        return reverse('store:part_detail', kwargs={'pk': self.pk})

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.primary_image_url:
            return self.primary_image_url
        return 'https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=600&q=80'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid / Confirmed'),
        ('processing', 'Processing Warehouse Pick'),
        ('shipped', 'Shipped / In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=32, unique=True, editable=False, db_index=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=25)
    
    shipping_address = models.CharField(max_length=255)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    postal_code = models.CharField('PIN Code', max_length=20)
    country = models.CharField(max_length=64, default='India')

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='paid')
    payment_method = models.CharField(max_length=50, default='UPI / Net Banking (Demo)')
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.order_number} - {self.customer_name}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"CC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:order_confirmation', kwargs={'order_number': self.order_number})


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    part = models.ForeignKey(Part, related_name='order_items', on_delete=models.PROTECT)
    part_name = models.CharField(max_length=150)
    part_sku = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.quantity}x {self.part_name} @ ₹{self.price}"

    @property
    def subtotal(self):
        return self.price * self.quantity
