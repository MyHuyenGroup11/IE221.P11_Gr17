from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.TrangChu, name='TrangChu'),
    path('search/', views.TimKiem, name='TimKiem'),
    path('update_item/', views.updateItem, name='update_item'),
    path('signin/', views.DangNhap, name='DangNhap'),
    path('personal-page/', views.TrangCaNhan, name='TrangCaNhan'),
    path('edit-personal-page/', views.EditTrangCaNhan, name='EditTrangCaNhan'),
    path('register/', views.DangKy, name='DangKy'),
    path('logout/', views.DangXuat, name='DangXuat'),
    path('cart/', views.GioHang, name='GioHang'),
    path('order/', views.DatHang, name='DatHang'),
    path('myorder/', views.DonHangCuaToi, name='DonHangCuaToi'),
    path('don-hang/huy/<int:order_id>/', views.HuyDonHang, name='cancel_order'),
    path('<str:cate_lv1_name>/', views.PList_Lv1, name='categories_products'),
    path('<str:cate_lv1_name>/<str:cate_lv2_name>/', views.PList_Lv2, name='categories_lv2'),
    path('<str:cate_lv1_name>/<str:cate_lv2_name>/<str:product_name>/', views.ChiTietSanPham, name='product_detail'),
]

# setting url của hình ảnh
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 