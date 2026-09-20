from django import forms
from .models import Order, Part


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm text-center quantity-input', 'style': 'max-width: 80px;'})
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_name', 'customer_email', 'customer_phone',
            'shipping_address', 'city', 'state', 'postal_code',
            'payment_method', 'notes'
        ]
        labels = {
            'postal_code': 'PIN Code',
        }
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rahul Sharma'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'rahul.sharma@example.in'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 98201 23456'}),
            'shipping_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Flat 402, Sea Green Apartments, Worli Sea Face'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mumbai'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Maharashtra'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '400018'}),
            'payment_method': forms.Select(
                choices=[
                    ('UPI (Google Pay / PhonePe / Paytm / BHIM)', 'UPI (Google Pay / PhonePe / Paytm / BHIM)'),
                    ('Credit / Debit / RuPay Card (Instant Authorization)', 'Credit / Debit / RuPay Card (Instant Authorization)'),
                    ('Net Banking (SBI / HDFC / ICICI / Axis)', 'Net Banking (SBI / HDFC / ICICI / Axis)'),
                    ('Dealership Account / Commercial Net-30', 'Dealership Account / Commercial Net-30'),
                    ('Pay Upon Workshop Pickup', 'Pay Upon Workshop Pickup'),
                ],
                attrs={'class': 'form-select'}
            ),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Special delivery notes, landmark, or garage access details...'}),
        }


class PartFilterForm(forms.Form):
    q = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control bg-dark border-secondary text-light', 'placeholder': 'Search parts by name, SKU, or brand...'})
    )
    category = forms.CharField(required=False, widget=forms.HiddenInput)
    in_stock = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ('-featured', 'Featured Highlights'),
            ('price', 'Price: Low to High'),
            ('-price', 'Price: High to Low'),
            ('name', 'Name: A to Z'),
            ('-stock', 'Highest Stock'),
        ],
        widget=forms.Select(attrs={'class': 'form-select bg-dark border-secondary text-light'})
    )


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = [
            'name', 'sku', 'category', 'brand', 'price', 'stock',
            'description', 'specifications', 'primary_image_url', 'image', 'featured'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Brembo GT High-Performance Front Brake Kit'}),
            'sku': forms.TextInput(attrs={'class': 'form-control font-monospace text-uppercase', 'placeholder': 'e.g. BRM-IN-330F'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Brembo Performance'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 48500.00', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 15'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'specifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g. Fitment: Mahindra XUV700 / Tata Safari / Hyundai Creta | Rotor: 330mm ventilated | Fluid: DOT 4'}),
            'primary_image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://images.unsplash.com/...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
