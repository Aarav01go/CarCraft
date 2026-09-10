import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q, Count
from .models import ServiceBay, Appointment
from .forms import AppointmentBookingForm, AppointmentStatusForm


class BookAppointmentView(CreateView):
    model = Appointment
    form_class = AppointmentBookingForm
    template_name = 'service/book_appointment.html'

    def get_initial(self):
        initial = super().get_initial()
        # Set default date to today or tomorrow
        initial['date'] = timezone.now().date()
        initial['time_slot'] = '08:00'
        # Check if pre-filled vehicle details from inventory detail page
        vehicle_param = self.request.GET.get('vehicle')
        vin_param = self.request.GET.get('vin')
        if vehicle_param:
            initial['vehicle_description'] = vehicle_param
        if vin_param:
            initial['vehicle_vin'] = vin_param
        return initial

    def form_valid(self, form):
        self.object = form.save()
        messages.success(
            self.request, 
            f"🎉 Service appointment confirmed for {self.object.customer_name}! "
            f"Assigned to {self.object.assigned_bay.name if self.object.assigned_bay else 'Workshop Bay'} on {self.object.date} at {self.object.get_time_slot_display()}."
        )
        return redirect('service:appointment_detail', pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bays'] = ServiceBay.objects.filter(is_active=True)
        context['time_slots'] = Appointment.TIME_SLOTS
        context['service_types'] = Appointment.SERVICE_TYPES
        context['service_costs'] = Appointment.SERVICE_COSTS
        return context


class BayBoardView(TemplateView):
    template_name = 'service/bay_board.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_str = self.request.GET.get('date')
        if date_str:
            try:
                selected_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                selected_date = timezone.now().date()
        else:
            selected_date = timezone.now().date()

        active_bays = list(ServiceBay.objects.filter(is_active=True).order_by('bay_number'))
        appointments = Appointment.objects.filter(
            date=selected_date
        ).exclude(status='cancelled').select_related('assigned_bay')

        # Build 2D matrix: [time_slot][bay_id] = appointment
        time_slots = Appointment.TIME_SLOTS
        board_data = []

        total_possible_slots = len(active_bays) * len(time_slots)
        booked_count = appointments.count()
        completed_count = appointments.filter(status='completed').count()
        in_progress_count = appointments.filter(status='in_progress').count()
        scheduled_count = appointments.filter(status='scheduled').count()

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
                    'appointment': appt
                })
            board_data.append(slot_row)

        context['selected_date'] = selected_date
        context['prev_date'] = selected_date - datetime.timedelta(days=1)
        context['next_date'] = selected_date + datetime.timedelta(days=1)
        context['today'] = timezone.now().date()
        context['active_bays'] = active_bays
        context['board_data'] = board_data
        context['stats'] = {
            'booked': booked_count,
            'completed': completed_count,
            'in_progress': in_progress_count,
            'scheduled': scheduled_count,
            'occupancy_rate': occupancy_rate,
            'total_slots': total_possible_slots,
        }
        return context


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'service/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 15

    def get_queryset(self):
        qs = Appointment.objects.select_related('assigned_bay').all()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        bay_id = self.request.GET.get('bay')
        date_filter = self.request.GET.get('date')

        if q:
            qs = qs.filter(
                Q(customer_name__icontains=q) |
                Q(customer_phone__icontains=q) |
                Q(vehicle_description__icontains=q) |
                Q(vehicle_vin__icontains=q)
            )
        if status:
            qs = qs.filter(status=status)
        if bay_id:
            qs = qs.filter(assigned_bay_id=bay_id)
        if date_filter:
            try:
                d = datetime.datetime.strptime(date_filter, '%Y-%m-%d').date()
                qs = qs.filter(date=d)
            except ValueError:
                pass

        return qs.order_by('date', 'time_slot')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bays'] = ServiceBay.objects.filter(is_active=True)
        context['statuses'] = Appointment.STATUS_CHOICES
        context['current_q'] = self.request.GET.get('q', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_bay'] = self.request.GET.get('bay', '')
        context['current_date'] = self.request.GET.get('date', '')
        return context


class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = 'service/appointment_detail.html'
    context_object_name = 'appointment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_form'] = AppointmentStatusForm(instance=self.object)
        return context


class UpdateAppointmentStatusView(View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        new_status = request.POST.get('status')
        internal_notes = request.POST.get('internal_notes')

        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            if internal_notes is not None:
                appointment.internal_notes = internal_notes
            appointment.save(update_fields=['status', 'internal_notes'])
            messages.success(request, f"Appointment #{appointment.id} status updated to: {appointment.get_status_display()}")

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'status': new_status,
                    'status_display': appointment.get_status_display(),
                    'ticket_class': appointment.status_ticket_class
                })

        next_url = request.POST.get('next') or appointment.get_absolute_url()
        return redirect(next_url)


class ApiAvailabilityCheckView(View):
    def get(self, request):
        date_str = request.GET.get('date')
        slot = request.GET.get('slot')

        if not date_str or not slot:
            return JsonResponse({'error': 'Missing date or slot parameter'}, status=400)

        try:
            check_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

        active_bays = ServiceBay.objects.filter(is_active=True)
        booked_bay_ids = Appointment.objects.filter(
            date=check_date,
            time_slot=slot
        ).exclude(status='cancelled').values_list('assigned_bay_id', flat=True)

        available_bays = active_bays.exclude(id__in=booked_bay_ids)
        available_count = available_bays.count()
        total_bays = active_bays.count()

        first_bay = available_bays.first()

        return JsonResponse({
            'date': date_str,
            'slot': slot,
            'total_bays': total_bays,
            'available_count': available_count,
            'is_fully_booked': available_count == 0,
            'suggested_bay': {
                'id': first_bay.id,
                'name': first_bay.name,
                'technician': first_bay.assigned_technician
            } if first_bay else None,
            'message': 'Available' if available_count > 0 else 'All bays fully booked for this time slot'
        })
