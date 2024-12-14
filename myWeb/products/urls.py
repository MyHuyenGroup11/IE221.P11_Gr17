from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.TrangChu, name='TrangChu')
]

# setting url của hình ảnh
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)