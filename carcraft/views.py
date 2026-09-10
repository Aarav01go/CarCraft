from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Sum, Count
from inventory.models import Vehicle
from store.models import Part, Category
from service.models import ServiceBay, Appointment


class HomeDashboardView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        all_vehicles = Vehicle.objects.all()
        available_vehicles = all_vehicles.filter(status='available')
        
        # Key metrics
        context['stats'] = {
            'total_vehicles': all_vehicles.count(),
            'available_vehicles': available_vehicles.count(),
            'pending_vehicles': all_vehicles.filter(status='pending').count(),
            'inventory_value': available_vehicles.aggregate(Sum('price'))['price__sum'] or 0,
            'parts_count': Part.objects.count(),
            'today_appointments_count': Appointment.objects.filter(date=today).exclude(status='cancelled').count(),
            'active_bays_count': ServiceBay.objects.filter(is_active=True).count(),
        }

        # Showroom highlights (featured + newest available)
        context['featured_vehicles'] = Vehicle.objects.filter(
            status='available'
        ).order_by('-featured', '-created_at')[:6]

        # Performance parts spotlight
        context['featured_parts'] = Part.objects.select_related('category').filter(
            stock__gt=0
        ).order_by('-featured', '-created_at')[:4]

        # Categories
        context['categories'] = Category.objects.annotate(parts_count=Count('parts'))[:6]

        # Workshop Today's snapshot
        active_bays = ServiceBay.objects.filter(is_active=True)
        today_appointments = Appointment.objects.filter(date=today).exclude(status='cancelled').select_related('assigned_bay')
        
        context['today'] = today
        context['bays'] = active_bays
        context['today_appointments'] = today_appointments
        
        return context
