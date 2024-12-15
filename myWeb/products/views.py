import json
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

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

    # Lấy món ăn
    product = get_object_or_404(Product, prod_name=product_name, prod_cate_lv1=cate_lv1, prod_cate_lv2=cate_lv2)

    # Lấy danh sách ảnh của món ăn
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
            # Lấy món ăn và gắn URL của ảnh avatar vào từng món ăn
            for product in keys:
                avatar = Product_Image.objects.filter(prod_name=product, is_avatar=True).first()
                product.avatar_url = avatar.ImageURL if avatar else None

                # Định dạng giá
                product.prod_price_formatted = "{:,.0f}".format(product.prod_price)

            # Phân trang với 12 món ăn mỗi trang
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
        # Lấy tất cả các món ăn trong giỏ hàng có tên của khách hàng hiện tại
        cart_items = Cart.objects.filter(cart_customer=customer)

        # Duyệt qua từng món ăn để lấy ảnh đại diện và định dạng giá
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

    total_selected_price = "{:,.0f}".format(Cart.calculate_selected_total(customer))   # Tính tổng tiền các sản phẩm được chọn

    
    # Kiểm tra giỏ hàng có rỗng hay không
    if not cart_items:
        empty_cart_message = "Bạn chưa bỏ gì vào giỏ hàng"
    else:
        empty_cart_message = ""

    context = {
        'cart_items': cart_items,
        'images': images_with_url,
        'empty_cart_message': empty_cart_message,  # Thêm thông báo nếu giỏ hàng trống
        'total_selected_price': total_selected_price,
    }
    return render(request, 'GioHang.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user
    product = Product.objects.get(id=productId)

    # Lấy món ăn trong giỏ hàng hoặc tạo mới nếu chưa có
    cart_item, created = Cart.objects.get_or_create(
        cart_customer=customer,
        cart_product=product
    )

    if action == 'select':
        cart_item.is_selected = not cart_item.is_selected  # Đảo trạng thái của is_selected
    elif action == 'add':
        if created:
            cart_item.cart_product_quantity = 1  # Nếu tạo mới, gán số lượng là 1
        else:
            cart_item.cart_product_quantity += 1  # Nếu đã tồn tại, tăng số lượng
    elif action == 'remove':
        cart_item.cart_product_quantity -= 1
        # Xóa món ăn nếu số lượng <= 0
        if cart_item.cart_product_quantity <= 0:
            cart_item.delete()
    elif action == 'remove_all':
        # Xóa món ăn bất kể số lượng
        cart_item.delete()

    # Lưu món ăn nếu không bị xóa
    if action in ['add', 'remove','select'] and cart_item.cart_product_quantity > 0:
        cart_item.save()

    return JsonResponse('Món ăn đã được cập nhật', safe=False)


def DangNhap(request):
    # Nếu đã được đăng nhập rồi thì trở lại trang chủ
    if request.user.is_authenticated:
        return redirect('TrangChu')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Đăng nhập thành công!', 'redirect_url': 'TrangChu'})
        else:
            return JsonResponse({'success': False, 'message': 'Tên đăng nhập hoặc mật khẩu chưa đúng'})

    return render(request, 'DangNhap.html')

def DangKy(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Đăng ký thành công!'})
        else:
            # Trả về các lỗi dạng JSON
            errors = {field: error.get_json_data() for field, error in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'DangKy.html', context)


def DangXuat(request):
    logout(request)
    return redirect('DangNhap')

def DatHang(request):
    customer = request.user  # Lấy thông tin người dùng đang đăng nhập
    if not customer.is_authenticated:
        return redirect('login')  # Chuyển hướng nếu người dùng chưa đăng nhập

    selected_cart_items = Cart.objects.filter(cart_customer=customer, is_selected=True)

    # Tạo context cho các sản phẩm được chọn và hình ảnh đại diện của sản phẩm
    images_with_url = []
    total_price = 0  # Tổng tiền phải trả

    for cart_item in selected_cart_items:
        product = cart_item.cart_product
        quantity = cart_item.cart_product_quantity
        price = product.prod_price

        item_total_price = price * quantity
        cart_item.item_total_price = "{:,.0f}".format(item_total_price)
        total_price += item_total_price

        # Định dạng giá sản phẩm
        product.prod_price_formatted = "{:,.0f}".format(price)

        avatar_image = Product_Image.objects.filter(prod_name=product, is_avatar=True).first()
        if avatar_image:
            images_with_url.append({
                'product_id': product.id,
                'url': avatar_image.ImageURL,
                'is_avatar': avatar_image.is_avatar,
            })

    total_price_formatted = "{:,.0f}".format(total_price)

    context = {
        'cart_items': selected_cart_items,
        'images': images_with_url,
        'total_price': total_price_formatted,
    }

    if request.method == 'POST':
        # Lấy thông tin nhận hàng từ POST request
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        if full_name and phone_number and address and payment_method:
            # Tạo đơn hàng mới
            order = Order(
                order_customer=customer,
                order_status='Đang xử lý',
                order_total=total_price,
                order_method=payment_method,
                
                order_receiver_name = full_name,
                order_receiver_phone = phone_number,
                order_adress = address,
            )
            order.save()

            # Thêm các sản phẩm vào đơn hàng
            for cart_item in selected_cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.cart_product,
                    quantity=cart_item.cart_product_quantity
                )

            # Xóa các sản phẩm đã được thêm vào đơn hàng khỏi giỏ hàng
            selected_cart_items.delete()

            # Hiển thị thông báo thành công
            messages.success(request, "Đặt hàng thành công!")
            return redirect('DonHangCuaToi')

        else:
            messages.error(request, "Vui lòng điền đầy đủ thông tin nhận hàng và chọn phương thức thanh toán.")

    return render(request, 'DatHang.html', context)

def DonHangCuaToi(request):
    customer = request.user
    order_list = Order.objects.filter(order_customer=customer)
    order_details = []

    # Lấy chi tiết từng đơn hàng
    for order in order_list:
        order_items = OrderItem.objects.filter(order=order)
        items_info = []
        for item in order_items:
            avatar_image = Product_Image.objects.filter(prod_name=item.product, is_avatar=True).first()
            image_url = avatar_image.ImageURL if avatar_image else ''  # URL của ảnh đại diện
            items_info.append({
                'product_name': item.product.prod_name,
                'quantity': item.quantity,
                'price': item.product.prod_price,
                'total_price': "{:,.0f}".format(item.quantity * item.product.prod_price),  # Tính tổng tiền
                'image_url': image_url,  # URL hình ảnh sản phẩm
            })
        order_details.append({
            'order_id': order.id,
            'order_date': order.order_date,
            'order_status': order.order_status,
            'order_total': "{:,.0f}".format(order.order_total),
            'order_method': order.order_method,
            'receiver_name': order.order_receiver_name,
            'receiver_phone': order.order_receiver_phone,
            'receiver_address': order.order_adress,
            'items': items_info,
        })

    context = {
        'order_details': order_details,
    }

    return render(request, 'DonHangCuaToi.html', context)