from django.urls import path
from .views import store_vehicle_details,home,get_vehicle_qr_image,render_get_qr,home1
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('',home, name='home'),
    path('store-vehicle/',store_vehicle_details,name='store-vehicle'),
    path('get-qr/',get_vehicle_qr_image,name="get-qr"),
    path('get-registered',render_get_qr,name="fetch"),
    path('qr/',home1,name="qr"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'Vehicles', 'static'))