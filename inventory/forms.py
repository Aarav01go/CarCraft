from django import forms
from .models import Vehicle, VehicleImage


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'vin', 'year', 'make', 'model', 'trim', 'type', 'status',
            'odometer', 'price', 'fuel_type', 'transmission', 'drivetrain',
            'exterior_color', 'interior_color', 'engine', 'horsepower',
            'primary_image_url', 'image', 'description', 'features', 'featured'
        ]
        widgets = {
            'vin': forms.TextInput(attrs={'class': 'form-control font-monospace text-uppercase', 'placeholder': '17-character VIN', 'maxlength': '17'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2024'}),
            'make': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mahindra'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. XUV700'}),
            'trim': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. AX7 L AWD'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'odometer': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 12500'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2450000.00', 'step': '0.01'}),
            'fuel_type': forms.Select(attrs={'class': 'form-select'}),
            'transmission': forms.Select(attrs={'class': 'form-select'}),
            'drivetrain': forms.Select(attrs={'class': 'form-select'}),
            'exterior_color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Everest White'}),
            'interior_color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Dual-Tone Ebony & Ivory'}),
            'engine': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2.0L mStallion Turbo-Petrol'}),
            'horsepower': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 197'}),
            'primary_image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://images.unsplash.com/...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed vehicle background, condition, and Indian service history...'}),
            'features': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Comma-separated: Level 2 ADAS, Panoramic Skyroof, Sony 3D Audio, Ventilated Seats'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_vin(self):
        vin = self.cleaned_data.get('vin', '').strip().upper()
        if len(vin) != 17:
            raise forms.ValidationError("VIN must be exactly 17 characters long.")
        return vin


class VehicleFilterForm(forms.Form):
    q = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control bg-dark border-secondary text-light', 'placeholder': 'Search by Make, Model, VIN, or Trim...'})
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Statuses')] + Vehicle.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select bg-dark border-secondary text-light'})
    )
    type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Body Types')] + Vehicle.TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select bg-dark border-secondary text-light'})
    )
    fuel_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Powertrains')] + Vehicle.FUEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select bg-dark border-secondary text-light'})
    )
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ('-created_at', 'Newest Arrivals'),
            ('price', 'Price: Low to High'),
            ('-price', 'Price: High to Low'),
            ('odometer', 'Odometer: Lowest First'),
            ('year', 'Year: Oldest First'),
            ('-year', 'Year: Newest First'),
        ],
        widget=forms.Select(attrs={'class': 'form-select bg-dark border-secondary text-light'})
    )
