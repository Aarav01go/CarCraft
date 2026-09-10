from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from .models import Vehicle, VehicleImage


class VehicleModelTests(TestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(
            vin='MA3ERFA12S0100456',
            year=2024,
            make='Maruti Suzuki',
            model='Baleno',
            trim='Alpha 1.2L',
            type='Hatchback',
            status='available',
            odometer=12000,
            price=Decimal('988000.00'),
            fuel_type='Petrol',
            transmission='Manual',
            drivetrain='FWD',
            features='360 HD View Camera, 9-inch SmartPlay Pro+, Head-up Display'
        )

    def test_vehicle_creation_and_properties(self):
        self.assertEqual(self.vehicle.title, "2024 Maruti Suzuki Baleno Alpha 1.2L")
        self.assertEqual(len(self.vehicle.feature_list), 3)
        self.assertEqual(self.vehicle.status_badge_class, 'badge-status-available')

    def test_vehicle_list_view(self):
        response = self.client.get(reverse('inventory:vehicle_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maruti Suzuki')
        self.assertContains(response, '9,88,000')

    def test_vehicle_filter(self):
        response = self.client.get(reverse('inventory:vehicle_list') + '?type=Hatchback&status=available')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['vehicles']), 1)

    def test_quick_status_change(self):
        response = self.client.post(
            reverse('inventory:quick_status', kwargs={'pk': self.vehicle.pk}),
            {'status': 'sold'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.status, 'sold')
