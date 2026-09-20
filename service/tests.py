import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import ServiceBay, Appointment
from .services import (
    get_active_bays,
    get_available_bays,
    get_bay_availability_status,
    build_bay_board_data,
    filter_appointments,
    parse_date_or_default,
)


class ServiceAppointmentTests(TestCase):
    def setUp(self):
        self.bay1 = ServiceBay.objects.create(
            bay_number=1,
            name='Bay 1 - Dyno & Diagnostics',
            assigned_technician='Rameshwar Patil',
            is_active=True
        )
        self.bay2 = ServiceBay.objects.create(
            bay_number=2,
            name='Bay 2 - Alignment & Suspension',
            assigned_technician='Arjun Nair',
            is_active=True
        )

    def test_booking_auto_assigns_available_bay(self):
        test_date = timezone.now().date() + datetime.timedelta(days=1)
        booking_url = reverse('service:book_appointment')

        post_data = {
            'customer_name': 'Aarav Singhania',
            'customer_email': 'aarav.singhania@apexmotors.in',
            'customer_phone': '+91 98201 55500',
            'vehicle_description': '2024 Tata Nexon EV Empowered Plus',
            'service_type': 'brake_performance',
            'date': test_date.strftime('%Y-%m-%d'),
            'time_slot': '08:00',
            'notes': 'High performance ceramic brake pads check requested.'
        }

        # First booking -> should get Bay 1
        response = self.client.post(booking_url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Appointment.objects.count(), 1)
        appt1 = Appointment.objects.first()
        self.assertEqual(appt1.assigned_bay, self.bay1)

        # Second booking for same slot -> should get Bay 2
        post_data['customer_name'] = 'Second Customer'
        response2 = self.client.post(booking_url, post_data, follow=True)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(Appointment.objects.count(), 2)
        appt2 = Appointment.objects.latest('id')
        self.assertEqual(appt2.assigned_bay, self.bay2)

        # Third booking for same slot -> All 2 bays are full -> Should show conflict error
        post_data['customer_name'] = 'Third Customer'
        response3 = self.client.post(booking_url, post_data)
        self.assertEqual(response3.status_code, 200)
        self.assertContains(response3, 'Workshop Bay Capacity Reached')

    def test_bay_board_view(self):
        response = self.client.get(reverse('service:bay_board'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bay 1 - Dyno &amp; Diagnostics')
        self.assertContains(response, 'Bay 2 - Alignment &amp; Suspension')

    def test_service_layer_and_api(self):
        test_date = timezone.now().date() + datetime.timedelta(days=2)
        bays = get_active_bays()
        self.assertEqual(bays.count(), 2)

        free_bays = get_available_bays(test_date, '08:00')
        self.assertEqual(free_bays.count(), 2)

        status = get_bay_availability_status(test_date, '08:00')
        self.assertEqual(status['total_bays'], 2)
        self.assertEqual(status['available_count'], 2)
        self.assertFalse(status['is_fully_booked'])
        self.assertEqual(status['suggested_bay']['id'], self.bay1.id)

        board = build_bay_board_data(test_date)
        self.assertEqual(len(board['board_data']), len(Appointment.TIME_SLOTS))

        api_url = reverse('service:api_availability') + f"?date={test_date.strftime('%Y-%m-%d')}&slot=08:00"
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['available_count'], 2)

        # Test filter_appointments and parse_date_or_default
        self.assertEqual(parse_date_or_default('invalid-date'), timezone.now().date())
        self.assertEqual(parse_date_or_default('2026-10-15'), datetime.date(2026, 10, 15))
        appt_qs = filter_appointments(Appointment.objects.all(), {'q': 'Tata', 'status': 'scheduled'})
        self.assertEqual(appt_qs.count(), 0)

