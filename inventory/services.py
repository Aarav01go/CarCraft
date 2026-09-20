from django.db.models import Q, Sum
from .models import Vehicle


def get_inventory_stats():
    """Aggregate vehicle inventory statistics for dashboards and list views."""
    all_vehicles = Vehicle.objects.all()
    available_vehicles = all_vehicles.filter(status='available')
    return {
        'total': all_vehicles.count(),
        'available': available_vehicles.count(),
        'pending': all_vehicles.filter(status='pending').count(),
        'sold': all_vehicles.filter(status='sold').count(),
        'total_value': available_vehicles.aggregate(Sum('price'))['price__sum'] or 0,
    }


def filter_vehicles(queryset, filter_data):
    """Filter and sort a vehicle queryset based on filter form data."""
    q = filter_data.get('q')
    status = filter_data.get('status')
    v_type = filter_data.get('type')
    fuel_type = filter_data.get('fuel_type')
    sort = filter_data.get('sort')

    if q:
        queryset = queryset.filter(
            Q(make__icontains=q) |
            Q(model__icontains=q) |
            Q(vin__icontains=q) |
            Q(trim__icontains=q) |
            Q(description__icontains=q)
        )
    if status:
        queryset = queryset.filter(status=status)
    if v_type:
        queryset = queryset.filter(type=v_type)
    if fuel_type:
        queryset = queryset.filter(fuel_type=fuel_type)

    if sort:
        queryset = queryset.order_by(sort)
    else:
        queryset = queryset.order_by('-created_at')

    return queryset
