from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from inventory.models import Vehicle
from store.models import Part, Category
from service.models import ServiceBay


class HomeDashboardTests(TestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(
            vin='MA3ERFA12S0100456',
            year=2024,
            make='Maruti Suzuki',
            model='Baleno',
            price=Decimal('988000.00'),
            status='available',
            featured=True
        )
        self.category = Category.objects.create(name='Brakes', slug='brakes')
        self.part = Part.objects.create(
            sku='BRK-100',
            name='Performance Brake Pad',
            category=self.category,
            price=Decimal('4500.00'),
            stock=10,
            featured=True
        )
        self.bay = ServiceBay.objects.create(
            bay_number=1,
            name='Bay 1',
            assigned_technician='Tech A',
            is_active=True
        )

    def test_home_dashboard_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Baleno')
        self.assertContains(response, 'Performance Brake Pad')
        self.assertEqual(response.context['stats']['total_vehicles'], 1)
        self.assertEqual(response.context['stats']['active_bays_count'], 1)
