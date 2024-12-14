from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def TrangChu(request):
    # Lấy 6 món ăn
    products = Product.objects.all()
    
    # Lấy sản phẩm và gắn URL của ảnh avatar vào từng sản phẩm
    for product in products:
        avatar = Product_Image.objects.filter(prod_name=product, is_avatar=True).first()
        product.avatar_url = avatar.ImageURL if avatar else None
    
     # Định dạng giá
        product.prod_price_formatted = "{:,.0f}".format(product.prod_price)

    # Cập nhật số lượng sản phẩm cho tất phân loại 2
    categories_lv2 = Category_lv2.objects.all()
    for category in categories_lv2:
        category.update_num_products()

    # Lấp top 14 phân loại 2 có nhiều sản phẩm nhất
    top_categories = Category_lv2.objects.all().order_by('-num_products')[:14]
        
    context = {
        'page_obj': products,
        'top_categories': top_categories,
    }
    return render(request, 'TrangChu.html', context)