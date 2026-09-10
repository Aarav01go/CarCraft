from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from .models import Vehicle, VehicleImage
from .forms import VehicleForm, VehicleFilterForm


class VehicleListView(ListView):
    model = Vehicle
    template_name = 'inventory/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 12

    def get_queryset(self):
        queryset = Vehicle.objects.all()
        self.form = VehicleFilterForm(self.request.GET)
        
        if self.form.is_valid():
            q = self.form.cleaned_data.get('q')
            status = self.form.cleaned_data.get('status')
            v_type = self.form.cleaned_data.get('type')
            fuel_type = self.form.cleaned_data.get('fuel_type')
            sort = self.form.cleaned_data.get('sort')

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
                if sort == 'mileage':
                    sort = 'odometer'
                elif sort == '-mileage':
                    sort = '-odometer'
                queryset = queryset.order_by(sort)
            else:
                queryset = queryset.order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_vehicles = Vehicle.objects.all()
        context['form'] = self.form
        context['stats'] = {
            'total': all_vehicles.count(),
            'available': all_vehicles.filter(status='available').count(),
            'pending': all_vehicles.filter(status='pending').count(),
            'sold': all_vehicles.filter(status='sold').count(),
            'total_value': all_vehicles.filter(status='available').aggregate(Sum('price'))['price__sum'] or 0,
        }
        context['types'] = Vehicle.TYPE_CHOICES
        context['current_type'] = self.request.GET.get('type', '')
        context['current_status'] = self.request.GET.get('status', '')
        return context


class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'inventory/vehicle_detail.html'
    context_object_name = 'vehicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery_images'] = self.object.gallery_images.all()
        context['similar_vehicles'] = Vehicle.objects.filter(
            type=self.object.type
        ).exclude(pk=self.object.pk)[:3]
        return context


class VehicleCreateView(CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'inventory/vehicle_form.html'

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, f"✨ Vehicle {self.object.title} successfully added to inventory!")
        return redirect(self.object.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Add New Vehicle"
        context['action_btn'] = "Add to Inventory"
        return context


class VehicleUpdateView(UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'inventory/vehicle_form.html'

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, f"✅ Vehicle {self.object.title} updated successfully.")
        return redirect(self.object.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit {self.object.title}"
        context['action_btn'] = "Save Changes"
        return context


class VehicleDeleteView(DeleteView):
    model = Vehicle
    template_name = 'inventory/vehicle_confirm_delete.html'
    success_url = reverse_lazy('inventory:vehicle_list')

    def delete(self, request, *args, **kwargs):
        vehicle = self.get_object()
        title = vehicle.title
        messages.warning(request, f"🗑️ Vehicle {title} (VIN: {vehicle.vin}) has been removed from inventory.")
        return super().delete(request, *args, **kwargs)


class QuickStatusChangeView(View):
    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Vehicle.STATUS_CHOICES):
            vehicle.status = new_status
            vehicle.save(update_fields=['status'])
            messages.info(request, f"Status for {vehicle.title} updated to: {vehicle.get_status_display()}")
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'status': new_status,
                    'status_display': vehicle.get_status_display(),
                    'badge_class': vehicle.status_badge_class
                })
        next_url = request.POST.get('next') or vehicle.get_absolute_url()
        return redirect(next_url)
