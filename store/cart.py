from decimal import Decimal
from django.conf import settings
from .models import Part


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, part, quantity=1, override_quantity=False):
        part_id = str(part.id)
        if part_id not in self.cart:
            self.cart[part_id] = {
                'quantity': 0,
                'price': str(part.price),
                'name': part.name,
                'sku': part.sku,
                'image_url': part.display_image,
                'max_stock': part.stock,
            }

        if override_quantity:
            qty = int(quantity)
        else:
            qty = self.cart[part_id]['quantity'] + int(quantity)

        # Cap by available stock
        qty = max(1, min(qty, part.stock)) if part.stock > 0 else 0
        self.cart[part_id]['quantity'] = qty
        self.cart[part_id]['price'] = str(part.price)
        self.save()

    def remove(self, part_id):
        part_id = str(part_id)
        if part_id in self.cart:
            del self.cart[part_id]
            self.save()

    def update_quantity(self, part_id, quantity):
        part_id = str(part_id)
        if part_id in self.cart:
            qty = int(quantity)
            if qty <= 0:
                self.remove(part_id)
            else:
                max_stock = self.cart[part_id].get('max_stock', 999)
                self.cart[part_id]['quantity'] = min(qty, max_stock)
                self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        part_ids = self.cart.keys()
        parts = Part.objects.filter(id__in=part_ids)
        cart_copy = self.cart.copy()

        parts_map = {str(p.id): p for p in parts}

        for part_id, item in cart_copy.items():
            item['part'] = parts_map.get(part_id)
            item['price_decimal'] = Decimal(item['price'])
            item['total_price'] = item['price_decimal'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_subtotal(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_tax(self):
        # 18% standard GST for automotive components
        return (self.get_subtotal() * Decimal('0.18')).quantize(Decimal('0.01'))

    def get_shipping(self):
        subtotal = self.get_subtotal()
        if subtotal == Decimal('0.00') or subtotal >= Decimal('2500.00'):
            return Decimal('0.00')
        return Decimal('250.00')

    def get_total_price(self):
        return self.get_subtotal() + self.get_tax() + self.get_shipping()
