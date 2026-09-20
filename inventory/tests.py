from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from .models import Vehicle
from .services import get_inventory_stats, filter_vehicles


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

    def test_vehicle_crud_flows(self):
        # 1. Detail View
        detail_url = reverse('inventory:vehicle_detail', kwargs={'pk': self.vehicle.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'MA3ERFA12S0100456')

        # 2. Create View
        add_url = reverse('inventory:vehicle_add')
        post_data = {
            'vin': 'MA3ERFA12S0100789',
            'year': 2024,
            'make': 'Tata',
            'model': 'Nexon',
            'trim': 'Creative Plus',
            'type': 'SUV',
            'status': 'available',
            'odometer': 5000,
            'price': '1350000.00',
            'fuel_type': 'Gasoline',
            'transmission': 'Manual',
            'drivetrain': 'FWD',
            'exterior_color': 'Daytona Grey',
            'interior_color': 'Black',
            'engine': '1.2L Turbo',
            'description': 'Excellent condition Nexon'
        }
        response = self.client.post(add_url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Vehicle.objects.count(), 2)

        # 3. Update View
        edit_url = reverse('inventory:vehicle_edit', kwargs={'pk': self.vehicle.pk})
        post_data['vin'] = self.vehicle.vin
        post_data['make'] = 'Maruti Suzuki'
        post_data['model'] = 'Baleno Alpha'
        response = self.client.post(edit_url, post_data)
        self.assertEqual(response.status_code, 302)
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.model, 'Baleno Alpha')

        # 4. Delete View
        delete_url = reverse('inventory:vehicle_delete', kwargs={'pk': self.vehicle.pk})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Vehicle.objects.filter(pk=self.vehicle.pk).count(), 0)

    def test_inventory_services(self):
        stats = get_inventory_stats()
        self.assertIn('total', stats)
        self.assertIn('available', stats)
        self.assertIn('total_value', stats)

        qs = filter_vehicles(Vehicle.objects.all(), {'q': 'Baleno', 'type': 'Hatchback', 'status': 'available'})
        self.assertEqual(qs.count(), 1)
