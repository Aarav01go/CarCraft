from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count
from inventory.models import Vehicle
from inventory.services import get_inventory_stats
from store.models import Part, Category
from service.models import Appointment
from service.services import get_active_bays


class HomeDashboardView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        inv_stats = get_inventory_stats()
        active_bays = get_active_bays()

        context['stats'] = {
            'total_vehicles': inv_stats['total'],
            'available_vehicles': inv_stats['available'],
            'pending_vehicles': inv_stats['pending'],
            'inventory_value': inv_stats['total_value'],
            'parts_count': Part.objects.count(),
            'today_appointments_count': Appointment.objects.filter(date=today).exclude(status='cancelled').count(),
            'active_bays_count': active_bays.count(),
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
        today_appointments = Appointment.objects.filter(date=today).exclude(status='cancelled').select_related('assigned_bay')

        context['today'] = today
        context['bays'] = active_bays
        context['today_appointments'] = today_appointments

        return context

