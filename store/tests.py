from decimal import Decimal
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from .models import Category, Part, Order
from .cart import Cart
from .forms import CheckoutForm
from .services import get_cart_summary, process_checkout, filter_parts, filter_orders


class StoreAndCartTests(TestCase):
    def setUp(self):
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

    def test_store_services(self):
        factory = RequestFactory()
        request = factory.get('/')
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        cart = Cart(request)
        cart.add(self.part, quantity=2)

        summary = get_cart_summary(cart)
        self.assertEqual(summary['subtotal'], Decimal('97000.00'))
        self.assertTrue('tax' in summary)
        self.assertTrue('shipping' in summary)

        # Insufficient stock test
        form = CheckoutForm({
            'customer_name': 'Test User',
            'customer_email': 'test@example.com',
            'customer_phone': '1234567890',
            'shipping_address': 'Address 1',
            'city': 'Mumbai',
            'state': 'MH',
            'postal_code': '400001',
            'payment_method': 'UPI'
        })
        self.assertTrue(form.is_valid())
        self.part.stock = 1
        self.part.save()

        order, error = process_checkout(form, cart)
        self.assertIsNone(order)
        self.assertIn('Insufficient stock', error)

        # Test filter_parts
        qs = filter_parts(Part.objects.all(), {'q': 'Brembo', 'in_stock': True, 'sort': 'price'}, category=self.category)
        self.assertEqual(qs.count(), 1)

        # Test filter_orders
        order_qs = filter_orders(Order.objects.all(), 'Rohit')
        self.assertEqual(order_qs.count(), 0)

    def test_catalog_and_cart_operations(self):
        # Catalog GET with query
        response = self.client.get(reverse('store:catalog') + '?q=Brembo&category=brakes&in_stock=1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Brembo GT 6-Piston Test Kit')

        # Add to cart
        self.client.post(reverse('store:cart_add', kwargs={'part_id': self.part.id}), {'quantity': 1})

        # Update cart
        update_url = reverse('store:cart_update', kwargs={'part_id': self.part.id})
        response = self.client.post(update_url, {'quantity': 3}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['cart_count'], 3)

        # Remove from cart
        remove_url = reverse('store:cart_remove', kwargs={'part_id': self.part.id})
        response = self.client.post(remove_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['cart_count'], 0)

        # Order history GET
        response = self.client.get(reverse('store:order_history'))
        self.assertEqual(response.status_code, 200)

