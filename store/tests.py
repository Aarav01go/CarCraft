from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Part, Order, OrderItem
from .cart import Cart


class StoreAndCartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='Braking Systems',
            slug='brakes'
        )
        self.part = Part.objects.create(
            sku='BRM-GT6-TEST',
            name='Brembo GT 6-Piston Test Kit',
            category=self.category,
            brand='Brembo Racing',
            price=Decimal('48500.00'),
            stock=5
        )

    def test_cart_add_and_checkout_flow(self):
        # 1. Add to cart via POST
        add_url = reverse('store:cart_add', kwargs={'part_id': self.part.id})
        response = self.client.post(add_url, {'quantity': 2}, follow=True)
        self.assertEqual(response.status_code, 200)

        # 2. Checkout view GET
        checkout_url = reverse('store:checkout')
        response = self.client.get(checkout_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Brembo GT 6-Piston Test Kit')

        # 3. Checkout POST
        post_data = {
            'customer_name': 'Rohit Deshmukh',
            'customer_email': 'rohit.deshmukh@apexindia.com',
            'customer_phone': '+91 98201 23456',
            'shipping_address': 'Flat 1204, Sea Breeze Towers, Worli Sea Face',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'postal_code': '400018',
            'payment_method': 'UPI (GPay / PhonePe / Paytm)',
            'notes': 'Please call on delivery.'
        }
        response = self.client.post(checkout_url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # 4. Verify order created and stock decremented from 5 to 3
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.customer_name, 'Rohit Deshmukh')
        self.assertEqual(order.items.count(), 1)

        self.part.refresh_from_db()
        self.assertEqual(self.part.stock, 3)  # Stock reduced by 2
