from django.contrib import admin

# Register your models here.

# Đăng ký cho các model
from .models import *
admin.site.register(Category_lv1)
admin.site.register(Category_lv2)
admin.site.register(Product)
admin.site.register(Product_Image)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)