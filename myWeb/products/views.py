from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator
# Create your views here.
def TrangChu(request):
    # Lấy 6 món ăn
    products = Product.objects.all()[:6]
    
    # Lấy món ăn và gắn URL của ảnh avatar vào từng món ăn
    for product in products:
        avatar = Product_Image.objects.filter(prod_name=product, is_avatar=True).first()
        product.avatar_url = avatar.ImageURL if avatar else None
    
    # Định dạng giá
        product.prod_price_formatted = "{:,.0f}".format(product.prod_price)

    # Cập nhật số lượng món ăn cho tất phân loại 2
    categories_lv2 = Category_lv2.objects.all()
    for category in categories_lv2:
        category.update_num_products()

    # Lấp top 14 phân loại 2 có nhiều món ăn nhất
    top_categories = Category_lv2.objects.all().order_by('-num_products')[:14]
        
    context = {
        'page_obj': products,
        'top_categories': top_categories,
    }
    return render(request, 'TrangChu.html', context)

def PList_Lv1(request, cate_lv1_name):
    # Lấy danh mục cấp 1 dựa trên tên
    cate_lv1 = get_object_or_404(Category_lv1, cate_1=cate_lv1_name)

    # Lấy danh sách các danh mục cấp 2 thuộc danh mục cấp 1
    categories_lv2 = Category_lv2.objects.filter(cate_1=cate_lv1)

    # Lấy món ăn thuộc danh mục cấp 2
    products = Product.objects.filter(prod_cate_lv2__in=categories_lv2)

    # Cập nhật số lượng món ăn của từng category_lv2
    for cate_lv2 in categories_lv2:
        cate_lv2.update_num_products()

    # Lấy món ăn và gắn URL của ảnh avatar vào từng món ăn
    for product in products:
        avatar = Product_Image.objects.filter(prod_name=product, is_avatar=True).first()
        product.avatar_url = avatar.ImageURL if avatar else None

        # Định dạng giá
        product.prod_price_formatted = "{:,.0f}".format(product.prod_price)  # xxx.xxx

    # Cập nhật breadcrumb
    breadcrumb = [
        {"name": "Trang chủ", "url": "/"},
        {"name": cate_lv1.cate_1, "url": f"/{cate_lv1.cate_1}/"}
    ]

    # Phân trang với 12 món ăn mỗi trang
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Xử lý hiển thị phân trang rút gọn
    total_pages = paginator.num_pages
    current_page = page_obj.number
    if total_pages <= 7:
        page_range = paginator.page_range
    else:
        if current_page <= 4:
            page_range = list(range(1, 6)) + ['...'] + [total_pages]
        elif current_page > total_pages - 4:
            page_range = [1] + ['...'] + list(range(total_pages - 4, total_pages + 1))
        else:
            page_range = (
                [1] + ['...']
                + list(range(current_page - 1, current_page + 2))
                + ['...']
                + [total_pages]
            )

    # Cập nhật context
    context = {
        'cate_lv1': cate_lv1,
        'categories_lv2': categories_lv2,
        'page_obj': page_obj,
        'page_range': page_range,
        'breadcrumb': breadcrumb
    }

    return render(request, 'PList_Lv1.html', context)

def PList_Lv2(request, cate_lv1_name, cate_lv2_name):
    # Lấy danh mục cấp 1 và cấp 2 dựa trên tên
    cate_lv1 = get_object_or_404(Category_lv1, cate_1=cate_lv1_name)
    cate_lv2 = get_object_or_404(Category_lv2, cate_2=cate_lv2_name, cate_1=cate_lv1)

    # Lấy món ăn thuộc danh mục cấp 2
    products = Product.objects.filter(prod_cate_lv2=cate_lv2)

    # Lấy món ăn và gắn URL của ảnh avatar vào từng món ăn
    for product in products:
        avatar = Product_Image.objects.filter(prod_name=product, is_avatar=True).first()
        product.avatar_url = avatar.ImageURL if avatar else None

        # Định dạng giá
        product.prod_price_formatted = "{:,.0f}".format(product.prod_price)

    # Cập nhật breadcrumb
    breadcrumb = [
        {"name": "Trang chủ", "url": "/"},
        {"name": cate_lv1.cate_1, "url": f"/{cate_lv1.cate_1}/"},
        {"name": cate_lv2.cate_2, "url": f"/{cate_lv1.cate_1}/{cate_lv2.cate_2}/"}
    ]


    # Phân trang với 12 món ăn mỗi trang
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Xử lý hiển thị phân trang rút gọn
    total_pages = paginator.num_pages
    current_page = page_obj.number
    if total_pages <= 7:
        page_range = paginator.page_range
    else:
        if current_page <= 4:
            page_range = list(range(1, 6)) + ['...'] + [total_pages]
        elif current_page > total_pages - 4:
            page_range = [1] + ['...'] + list(range(total_pages - 4, total_pages + 1))
        else:
            page_range = (
                [1] + ['...']
                + list(range(current_page - 1, current_page + 2))
                + ['...']
                + [total_pages]
            )

    # Cập nhật context
    context = {
        'cate_lv1': cate_lv1,
        'cate_lv2': cate_lv2,
        'page_obj': page_obj,
        'page_range': page_range,
        'breadcrumb': breadcrumb
    }

    return render(request, 'PList_Lv2.html', context)

def ChiTietSanPham(request, cate_lv1_name, cate_lv2_name, product_name):
    # Lấy danh mục cấp 1 và cấp 2 dựa trên tên
    cate_lv1 = get_object_or_404(Category_lv1, cate_1=cate_lv1_name)
    cate_lv2 = get_object_or_404(Category_lv2, cate_2=cate_lv2_name, cate_1=cate_lv1)

    # Lấy sản phẩm
    product = get_object_or_404(Product, prod_name=product_name, prod_cate_lv1=cate_lv1, prod_cate_lv2=cate_lv2)

    # Lấy danh sách ảnh của sản phẩm
    images = Product_Image.objects.filter(prod_name=product)
    images_with_url = [{'url': img.ImageURL, 'is_avatar': img.is_avatar} for img in images]
    
    # Định dạng giá
    product.prod_price_formatted = "{:,.0f}".format(product.prod_price)
    
    # Cập nhật breadcrumb
    breadcrumb = [
        {"name": "Trang chủ", "url": "/"},
        {"name": cate_lv1.cate_1, "url": f"/{cate_lv1.cate_1}/"},
        {"name": cate_lv2.cate_2, "url": f"/{cate_lv1.cate_1}/{cate_lv2.cate_2}/"}
    ]
    
    context = {
        'cate_lv1': cate_lv1,
        'cate_lv2': cate_lv2,
        'product': product,
        'images': images_with_url,
        'breadcrumb': breadcrumb

    }
    return render(request, 'ChiTietSanPham.html', context)

def TimKiem(request):
    if request.method == "POST":
        searched = request.POST.get("searched", "").strip()
        if not searched:
            return redirect('TrangChu')  # Redirect về trang chủ nếu không có gì được tìm kiếm

        keys = Product.objects.filter(prod_name__icontains=searched)

        if not keys.exists():
            no_results_message = "Không có kết quả trùng khớp cho tìm kiếm của bạn."
            context = {
                'no_results_message': no_results_message if not keys.exists() else None,
                'searched': searched,
            }
            return render(request, 'TimKiem.html', context)
        else:
            # Lấy sản phẩm và gắn URL của ảnh avatar vào từng sản phẩm
            for product in keys:
                avatar = Product_Image.objects.filter(prod_name=product, is_avatar=True).first()
                product.avatar_url = avatar.ImageURL if avatar else None

                # Định dạng giá
                product.prod_price_formatted = "{:,.0f}".format(product.prod_price)

            # Phân trang với 12 sản phẩm mỗi trang
            paginator = Paginator(keys, 12)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            # Xử lý hiển thị phân trang rút gọn
            total_pages = paginator.num_pages
            current_page = page_obj.number
            if total_pages <= 7:
                page_range = paginator.page_range
            else:
                if current_page <= 4:
                    page_range = list(range(1, 6)) + ['...'] + [total_pages]
                elif current_page > total_pages - 4:
                    page_range = [1] + ['...'] + list(range(total_pages - 4, total_pages + 1))
                else:
                    page_range = (
                        [1] + ['...']
                        + list(range(current_page - 1, current_page + 2))
                        + ['...']
                        + [total_pages]
                    )

        context = {
            'page_obj': page_obj,
            'page_range': page_range,
            'searched': searched,
            'no_results_message': no_results_message if not keys.exists() else None,
        }
        return render(request, 'TimKiem.html', context)

def GioHang(request):  
    cart_items = []
    images_with_url = []

    if request.user.is_authenticated:
        customer = request.user
        # Lấy tất cả các sản phẩm trong giỏ hàng có tên của khách hàng hiện tại
        cart_items = Cart.objects.filter(cart_customer=customer)

        # Duyệt qua từng sản phẩm để lấy ảnh đại diện và định dạng giá
        for cart_item in cart_items:
            product = cart_item.cart_product

            # Định dạng giá
            product.prod_price_formatted = "{:,.0f}".format(product.prod_price)

            # Lấy ảnh đại diện
            avatar_image = Product_Image.objects.filter(
                prod_name=product, is_avatar=True
            ).first()  # Lấy ảnh avatar đầu tiên nếu có

            if avatar_image:
                images_with_url.append({
                    'product_id': product.id,
                    'url': avatar_image.ImageURL,
                    'is_avatar': avatar_image.is_avatar,
                })

    # Kiểm tra giỏ hàng có rỗng hay không
    if not cart_items:
        empty_cart_message = "Bạn chưa bỏ gì vào giỏ hàng"
    else:
        empty_cart_message = ""

    context = {
        'cart_items': cart_items,
        'images': images_with_url,
        'empty_cart_message': empty_cart_message,  # Thêm thông báo nếu giỏ hàng trống
    }
    return render(request, 'GioHang.html', context)