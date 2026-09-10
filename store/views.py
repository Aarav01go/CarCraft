from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db import transaction
from django.db.models import Q, Count
from django.http import JsonResponse
from .models import Part, Category, Order, OrderItem
from .forms import AddToCartForm, CheckoutForm, PartFilterForm, PartForm
from .cart import Cart


class CatalogView(ListView):
    model = Part
    template_name = 'store/catalog.html'
    context_object_name = 'parts'
    paginate_by = 12

    def get_queryset(self):
        queryset = Part.objects.select_related('category').all()
        self.form = PartFilterForm(self.request.GET)
        self.selected_category = None

        category_slug = self.request.GET.get('category')
        if category_slug:
            self.selected_category = Category.objects.filter(slug=category_slug).first()
            if self.selected_category:
                queryset = queryset.filter(category=self.selected_category)

        if self.form.is_valid():
            q = self.form.cleaned_data.get('q')
            in_stock = self.form.cleaned_data.get('in_stock')
            sort = self.form.cleaned_data.get('sort')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['categories'] = Category.objects.annotate(parts_count=Count('parts')).all()
        context['selected_category'] = self.selected_category
        context['total_parts_count'] = Part.objects.count()
        context['in_stock_count'] = Part.objects.filter(stock__gt=0).count()
        return context


class PartDetailView(DetailView):
    model = Part
    template_name = 'store/part_detail.html'
    context_object_name = 'part'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_to_cart_form'] = AddToCartForm()
        context['related_parts'] = Part.objects.filter(
            category=self.object.category
        ).exclude(pk=self.object.pk)[:4]
        return context


class CartDetailView(TemplateView):
    template_name = 'store/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        context['subtotal'] = cart.get_subtotal()
        context['tax'] = cart.get_tax()
        context['shipping'] = cart.get_shipping()
        context['total'] = cart.get_total_price()
        return context


class AddToCartView(View):
    def post(self, request, part_id):
        cart = Cart(request)
        part = get_object_or_404(Part, id=part_id)
        form = AddToCartForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            qty = cd['quantity']
            override = cd['override']
        else:
            qty = 1
            override = False

        if part.stock <= 0:
            messages.error(request, f"Sorry, {part.name} is currently out of stock.")
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Out of stock'}, status=400)
            return redirect('store:catalog')

        cart.add(part=part, quantity=qty, override_quantity=override)
        messages.success(request, f"🛒 Added {qty}x {part.name} to your cart!")

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': len(cart),
                'subtotal': str(cart.get_subtotal()),
                'total': str(cart.get_total_price()),
                'part_name': part.name,
                'message': f"Added {qty}x {part.name} to cart"
            })

        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('store:cart_detail')
        return redirect(next_url)


class UpdateCartView(View):
    def post(self, request, part_id):
        cart = Cart(request)
        quantity = request.POST.get('quantity', 1)
        try:
            qty = int(quantity)
            cart.update_quantity(part_id=part_id, quantity=qty)
            messages.info(request, "Cart updated.")
        except ValueError:
            messages.error(request, "Invalid quantity provided.")

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': len(cart),
                'subtotal': str(cart.get_subtotal()),
                'tax': str(cart.get_tax()),
                'shipping': str(cart.get_shipping()),
                'total': str(cart.get_total_price())
            })

        return redirect('store:cart_detail')


class RemoveFromCartView(View):
    def post(self, request, part_id):
        cart = Cart(request)
        cart.remove(part_id=part_id)
        messages.warning(request, "Item removed from cart.")

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': len(cart),
                'subtotal': str(cart.get_subtotal()),
                'total': str(cart.get_total_price())
            })

        return redirect('store:cart_detail')


class CheckoutView(View):
    def get(self, request):
        cart = Cart(request)
        if len(cart) == 0:
            messages.warning(request, "Your cart is currently empty. Browse our catalog to add parts.")
            return redirect('store:catalog')

        form = CheckoutForm()
        return render(request, 'store/checkout.html', {
            'form': form,
            'cart': cart,
            'subtotal': cart.get_subtotal(),
            'tax': cart.get_tax(),
            'shipping': cart.get_shipping(),
            'total': cart.get_total_price(),
        })

    def post(self, request):
        cart = Cart(request)
        if len(cart) == 0:
            messages.warning(request, "Your cart is empty.")
            return redirect('store:catalog')

        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Verify stock for all items
                    for item in cart:
                        part = item['part']
                        if not part or part.stock < item['quantity']:
                            raise ValueError(
                                f"Insufficient stock for {part.name if part else 'Item'}. "
                                f"Requested: {item['quantity']}, Available: {part.stock if part else 0}"
                            )

                    # Create order
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
                        # Decrement stock
                        part.stock -= item['quantity']
                        part.save(update_fields=['stock'])

                    # Clear cart after successful transaction
                    cart.clear()
                    messages.success(request, f"🎉 Order #{order.order_number} confirmed! Thank you for your purchase.")
                    return redirect('store:order_confirmation', order_number=order.order_number)

            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"An unexpected error occurred during checkout: {str(e)}")

        return render(request, 'store/checkout.html', {
            'form': form,
            'cart': cart,
            'subtotal': cart.get_subtotal(),
            'tax': cart.get_tax(),
            'shipping': cart.get_shipping(),
            'total': cart.get_total_price(),
        })


class OrderConfirmationView(DetailView):
    model = Order
    template_name = 'store/order_confirmation.html'
    context_object_name = 'order'
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'


class OrderHistoryView(ListView):
    model = Order
    template_name = 'store/order_history.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        qs = Order.objects.prefetch_related('items').all()
        if query:
            qs = qs.filter(
                Q(order_number__icontains=query) |
                Q(customer_email__icontains=query) |
                Q(customer_name__icontains=query) |
                Q(customer_phone__icontains=query)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class PartCreateView(CreateView):
    model = Part
    form_class = PartForm
    template_name = 'store/part_form.html'
    success_url = reverse_lazy('store:catalog')

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, f"✨ Part {self.object.name} added to catalog!")
        return redirect(self.object.get_absolute_url())


class PartUpdateView(UpdateView):
    model = Part
    form_class = PartForm
    template_name = 'store/part_form.html'

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, f"✅ Part {self.object.name} updated successfully.")
        return redirect(self.object.get_absolute_url())
