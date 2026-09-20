import datetime
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, View, TemplateView
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Appointment
from .forms import AppointmentBookingForm, AppointmentStatusForm
from .services import (
    get_active_bays,
    get_bay_availability_status,
    build_bay_board_data,
    parse_date_or_default,
    filter_appointments,
)


class BookAppointmentView(CreateView):
    model = Appointment
    form_class = AppointmentBookingForm
    template_name = 'service/book_appointment.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['date'] = timezone.now().date()
        initial['time_slot'] = '08:00'
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
        context['bays'] = get_active_bays()
        context['time_slots'] = Appointment.TIME_SLOTS
        context['service_types'] = Appointment.SERVICE_TYPES
        context['service_costs'] = Appointment.SERVICE_COSTS
        return context


class BayBoardView(TemplateView):
    template_name = 'service/bay_board.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_date = parse_date_or_default(self.request.GET.get('date'))

        board_context = build_bay_board_data(selected_date)
        context.update(board_context)
        context['selected_date'] = selected_date
        context['prev_date'] = selected_date - datetime.timedelta(days=1)
        context['next_date'] = selected_date + datetime.timedelta(days=1)
        context['today'] = timezone.now().date()
        return context


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'service/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 15

    def get_queryset(self):
        qs = Appointment.objects.select_related('assigned_bay').all()
        return filter_appointments(qs, self.request.GET)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bays'] = get_active_bays()
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

        check_date = parse_date_or_default(date_str, default=False)
        if not check_date:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

        status_data = get_bay_availability_status(check_date, slot)
        return JsonResponse({
            'date': date_str,
            'slot': slot,
            'total_bays': status_data['total_bays'],
            'available_count': status_data['available_count'],
            'is_fully_booked': status_data['is_fully_booked'],
            'suggested_bay': status_data['suggested_bay'],
            'message': 'Available' if status_data['available_count'] > 0 else 'All bays fully booked for this time slot'
        })
