from django.db import transaction
from django.db.models import Q
from .models import OrderItem


def filter_parts(queryset, filter_data=None, category=None):
    """Filter and sort a parts queryset based on search form data and optional category."""
    if category:
        queryset = queryset.filter(category=category)

    if not filter_data:
        return queryset.order_by('-featured', 'name')

    q = filter_data.get('q')
    in_stock = filter_data.get('in_stock')
    sort = filter_data.get('sort')

    if q:
        queryset = queryset.filter(
            Q(name__icontains=q) |
            Q(sku__icontains=q) |
            Q(brand__icontains=q) |
            Q(description__icontains=q)
        )
    if in_stock:
        queryset = queryset.filter(stock__gt=0)
    if sort:
        queryset = queryset.order_by(sort)
    else:
        queryset = queryset.order_by('-featured', 'name')

    return queryset


def filter_orders(queryset, query=None):
    """Filter orders by search query matching order number, customer name, email, or phone."""
    if query:
        query = query.strip()
        queryset = queryset.filter(
            Q(order_number__icontains=query) |
            Q(customer_email__icontains=query) |
            Q(customer_name__icontains=query) |
            Q(customer_phone__icontains=query)
        )
    return queryset


def get_cart_summary(cart):
    """Return monetary summary metrics for the given cart."""
    return {
        'cart': cart,
        'subtotal': cart.get_subtotal(),
        'tax': cart.get_tax(),
        'shipping': cart.get_shipping(),
        'total': cart.get_total_price(),
    }


def process_checkout(form, cart):
    """
    Atomically validate stock, create the Order and OrderItems, decrement stock,
    and clear the cart.

    Returns:
        tuple: (order, None) on success, or (None, str(error_message)) on failure.
    """
    if len(cart) == 0:
        return None, "Your cart is empty."

    try:
        with transaction.atomic():
            # Validate stock for all items upfront
            for item in cart:
                part = item['part']
                if not part or part.stock < item['quantity']:
                    part_title = part.name if part else 'Item'
                    avail = part.stock if part else 0
                    raise ValueError(
                        f"Insufficient stock for {part_title}. Requested: {item['quantity']}, Available: {avail}"
                    )

            # Create order record
            order = form.save(commit=False)
            order.total_amount = cart.get_total_price()
            order.save()

            # Create order items & decrement stock
            for item in cart:
                part = item['part']
                OrderItem.objects.create(
                    order=order,
                    part=part,
                    part_name=part.name,
                    part_sku=part.sku,
                    price=item['price_decimal'],
                    quantity=item['quantity']
                )
                part.stock -= item['quantity']
                part.save(update_fields=['stock'])

            # Clear session cart
            cart.clear()
            return order, None

    except ValueError as e:
        return None, str(e)
    except Exception as e:
        return None, f"An unexpected error occurred during checkout: {str(e)}"
