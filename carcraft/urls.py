"""
URL configuration for CarCraft Dealership Suite.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import HomeDashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeDashboardView.as_view(), name='home'),
    path('inventory/', include('inventory.urls', namespace='inventory')),
    path('store/', include('store.urls', namespace='store')),
    path('service/', include('service.urls', namespace='service')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
    urlpatterns += staticfiles_urlpatterns()
