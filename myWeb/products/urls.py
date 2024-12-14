from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.TrangChu, name='TrangChu'),
    
    path('<str:cate_lv1_name>/', views.PList_Lv1, name='categories_products'),
]

# setting url của hình ảnh
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)