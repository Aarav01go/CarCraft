from django.contrib import admin
from .models import ServiceBay, Appointment


@admin.register(ServiceBay)
class ServiceBayAdmin(admin.ModelAdmin):
    list_display = ['bay_number', 'name', 'assigned_technician', 'specialty', 'is_active']
    list_editable = ['is_active', 'assigned_technician']
    search_fields = ['name', 'assigned_technician', 'specialty']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer_name', 'customer_phone', 'vehicle_description',
        'service_type', 'date', 'time_slot', 'assigned_bay', 'status', 'estimated_cost'
    ]
    list_filter = ['status', 'service_type', 'date', 'assigned_bay']
    search_fields = ['customer_name', 'customer_email', 'customer_phone', 'vehicle_description', 'vehicle_vin']
    list_editable = ['status', 'assigned_bay']
    date_hierarchy = 'date'
    actions = ['mark_in_progress', 'mark_completed', 'mark_cancelled']

    @admin.action(description='Mark selected appointments as In Progress')
    def mark_in_progress(self, request, queryset):
        queryset.update(status='in_progress')

    @admin.action(description='Mark selected appointments as Completed')
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')

    @admin.action(description='Mark selected appointments as Cancelled')
    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
