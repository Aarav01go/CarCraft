from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.VehicleListView.as_view(), name='vehicle_list'),
    path('add/', views.VehicleCreateView.as_view(), name='vehicle_add'),
    path('<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    path('<int:pk>/edit/', views.VehicleUpdateView.as_view(), name='vehicle_edit'),
    path('<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),
    path('<int:pk>/quick-status/', views.QuickStatusChangeView.as_view(), name='quick_status'),
]
