from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('', views.BayBoardView.as_view(), name='bay_board'),
    path('book/', views.BookAppointmentView.as_view(), name='book_appointment'),
    path('appointments/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointments/<int:pk>/update-status/', views.UpdateAppointmentStatusView.as_view(), name='update_status'),
    path('api/availability/', views.ApiAvailabilityCheckView.as_view(), name='api_availability'),
]
