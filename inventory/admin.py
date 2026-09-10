from django.contrib import admin
from .models import Vehicle, VehicleImage


class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 1
    fields = ['image', 'image_url', 'caption', 'display_order']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'vin', 'type', 'fuel_type', 'price', 
        'odometer', 'status', 'featured', 'created_at'
    ]
    list_filter = ['status', 'type', 'fuel_type', 'transmission', 'year', 'featured']
    search_fields = ['vin', 'make', 'model', 'trim', 'engine', 'exterior_color']
    list_editable = ['status', 'featured', 'price']
    inlines = [VehicleImageInline]
    date_hierarchy = 'created_at'
    actions = ['mark_as_available', 'mark_as_pending', 'mark_as_sold']

    @admin.action(description='Mark selected vehicles as Available')
    def mark_as_available(self, request, queryset):
        queryset.update(status='available')

    @admin.action(description='Mark selected vehicles as Pending Sale')
    def mark_as_pending(self, request, queryset):
        queryset.update(status='pending')

    @admin.action(description='Mark selected vehicles as Sold')
    def mark_as_sold(self, request, queryset):
        queryset.update(status='sold')


@admin.register(VehicleImage)
class VehicleImageAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'caption', 'display_order', 'display_url']
    list_filter = ['vehicle__make']
