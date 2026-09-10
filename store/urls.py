from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.CatalogView.as_view(), name='catalog'),
    path('part/<int:pk>/', views.PartDetailView.as_view(), name='part_detail'),
    path('part/add/', views.PartCreateView.as_view(), name='part_add'),
    path('part/<int:pk>/edit/', views.PartUpdateView.as_view(), name='part_edit'),
    
    # Cart Operations
    path('cart/', views.CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:part_id>/', views.AddToCartView.as_view(), name='cart_add'),
    path('cart/update/<int:part_id>/', views.UpdateCartView.as_view(), name='cart_update'),
    path('cart/remove/<int:part_id>/', views.RemoveFromCartView.as_view(), name='cart_remove'),
    
    # Checkout & Orders
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('orders/confirmation/<str:order_number>/', views.OrderConfirmationView.as_view(), name='order_confirmation'),
    path('orders/', views.OrderHistoryView.as_view(), name='order_history'),
]
