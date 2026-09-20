import datetime
from django.db.models import Q
from django.utils import timezone
from .models import ServiceBay, Appointment


def parse_date_or_default(date_str, default=None):
    """Safely parse a 'YYYY-MM-DD' date string or return default (defaults to today)."""
    if default is None:
        default = timezone.now().date()
    if not date_str:
        return default
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return default


def filter_appointments(queryset, filter_data=None):
    """Filter appointment queryset by search term, status, bay, and date."""
    if not filter_data:
        return queryset.order_by('date', 'time_slot')

    q = filter_data.get('q')
    status = filter_data.get('status')
    bay_id = filter_data.get('bay')
    date_filter = filter_data.get('date')

    if q:
        queryset = queryset.filter(
            Q(customer_name__icontains=q) |
            Q(customer_phone__icontains=q) |
            Q(vehicle_description__icontains=q) |
            Q(vehicle_vin__icontains=q)
        )
    if status:
        queryset = queryset.filter(status=status)
    if bay_id:
        queryset = queryset.filter(assigned_bay_id=bay_id)
    if date_filter:
        parsed_date = parse_date_or_default(date_filter, default=False)
        if parsed_date:
            queryset = queryset.filter(date=parsed_date)

    return queryset.order_by('date', 'time_slot')


def get_active_bays():
    """Return active service bays ordered by bay number."""
    return ServiceBay.objects.filter(is_active=True).order_by('bay_number')


def get_available_bays(booking_date, time_slot, exclude_appointment_id=None):
    """
    Return queryset of active ServiceBays that are free for the given date and time slot.
    Excludes cancelled appointments.
    """
    active_bays = get_active_bays()
    if not active_bays.exists():
        return active_bays.none()

    booked_bay_query = Appointment.objects.filter(
        date=booking_date,
        time_slot=time_slot
    ).exclude(status='cancelled')

    if exclude_appointment_id:
        booked_bay_query = booked_bay_query.exclude(pk=exclude_appointment_id)

    booked_bay_ids = booked_bay_query.values_list('assigned_bay_id', flat=True)
    return active_bays.exclude(id__in=booked_bay_ids)


def get_bay_availability_status(check_date, time_slot):
    """
    Compute bay capacity metrics and suggested bay for a specific date and slot.
    """
    active_bays = get_active_bays()
    total_bays = active_bays.count()
    available_bays = get_available_bays(check_date, time_slot)
    available_count = available_bays.count()
    first_bay = available_bays.first()

    return {
        'total_bays': total_bays,
        'available_count': available_count,
        'is_fully_booked': available_count == 0,
        'suggested_bay': {
            'id': first_bay.id,
            'name': first_bay.name,
            'technician': first_bay.assigned_technician,
        } if first_bay else None,
    }


def build_bay_board_data(selected_date):
    """
    Construct the 2D time_slot x bay_id matrix and aggregate metrics for the bay board.
    """
    active_bays = list(get_active_bays())
    appointments = list(
        Appointment.objects.filter(date=selected_date)
        .exclude(status='cancelled')
        .select_related('assigned_bay')
    )

    time_slots = Appointment.TIME_SLOTS
    board_data = []

    total_possible_slots = len(active_bays) * len(time_slots)
    booked_count = len(appointments)
    completed_count = sum(1 for a in appointments if a.status == 'completed')
    in_progress_count = sum(1 for a in appointments if a.status == 'in_progress')
    scheduled_count = sum(1 for a in appointments if a.status == 'scheduled')

    occupancy_rate = int((booked_count / total_possible_slots * 100)) if total_possible_slots > 0 else 0

    for slot_code, slot_label in time_slots:
        slot_row = {
            'code': slot_code,
            'label': slot_label,
            'bays': []
        }
        for bay in active_bays:
            appt = next((a for a in appointments if a.time_slot == slot_code and a.assigned_bay_id == bay.id), None)
            slot_row['bays'].append({
                'bay': bay,
                'appointment': appt,
            })
        board_data.append(slot_row)

    stats = {
        'booked': booked_count,
        'completed': completed_count,
        'in_progress': in_progress_count,
        'scheduled': scheduled_count,
        'occupancy_rate': occupancy_rate,
        'total_slots': total_possible_slots,
    }

    return {
        'active_bays': active_bays,
        'board_data': board_data,
        'stats': stats,
    }
