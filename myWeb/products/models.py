from django.db import models
from django.contrib.auth.models import User



# Phân loại món ăn lv1: Khai vị, Món chính, Món tráng miệng, Nước uống
class Category_lv1(models.Model):
    UNIT_TYPE_CHOICES = [
        ('Khai vị', 'Khai vị'),
        ('Món chính', 'Món chính'),
        ('Món tráng miệng', 'Món tráng miệng'),
        ('Nước uống', 'Nước uống'),
    ]
    cate_1 = models.CharField(max_length=500, choices=UNIT_TYPE_CHOICES)
    
    def __str__(self) -> str:
        return self.cate_1

# Phân loại sản phẩm lv2 theo từng cái lv1
class Category_lv2(models.Model):
    # Khóa ngoại tham chiếu đến phân loại lv1
    cate_1 = models.ForeignKey(Category_lv1, on_delete=models.SET_NULL, null=True, blank=False)
    cate_2 = models.CharField(max_length=500)
    
    num_products = models.IntegerField(default=0) # Số loại món ăn thuộc danh mục cấp 2

    def __str__(self) -> str:
        return self.cate_2
    
    # Cập nhật số loại món ăn trong danh mục cấp 2.
    def update_num_products(self):  
        self.num_products = Product.objects.filter(prod_cate_lv2=self).count()
        self.save()

# Một món ăn gồm: Tên, giá, phân loại lv1, phân loại lv2, thông tin món ăn
class Product(models.Model):
    prod_name = models.CharField(max_length=500)
    prod_price = models.IntegerField()
    prod_cate_lv1 = models.ForeignKey(Category_lv1, on_delete=models.SET_NULL, null=True, blank=False)
    prod_cate_lv2 = models.ForeignKey(Category_lv2, on_delete=models.SET_NULL, null=True, blank=False)
    prod_description = models.CharField(max_length=500,null=True, blank=False)

    def __str__(self) -> str:
        return self.prod_name
    
# Ảnh của món ăn: 1 món ăn có thể có nhiều ảnh, và 1 ảnh trong số đó là avatar của món ăn
class Product_Image(models.Model):
    prod_name = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False)
    prod_image = models.ImageField(null=True, blank=False)
    is_avatar = models.BooleanField(default=False)

    def __str__(self):
        # Kiểm tra nếu có liên kết tới món ăn
        if self.prod_name:
            # Nếu là avatar thì trả về avatar + tên món ăn
            if self.is_avatar:
                return f"avatar_{self.prod_name.prod_name}" 
            return self.prod_name.prod_name  # Còn không thì chỉ tên món ăn
        return "Unknown Product Image"  # Dự phòng nếu không có món ăn nào
    
    # Trả về url của ảnh của món ăn hoặc trống để ngừa crash
    @property
    def ImageURL(self):
        try:
            url = self.prod_image.url
        except :
            url = ''
        return url

# Giỏ hàng: Giỏ hàng của 1 user chứa món ăn, số lượng món ăn đó , và 1 biến để xác định món đó có được chọn không
class Cart(models.Model):
    cart_customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    cart_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False)
    cart_product_quantity = models.IntegerField(default=1)
    is_selected = models.BooleanField(default=False)  # Trạng thái chọn/bỏ chọn sản phẩm
    
    def __str__(self) -> str:
        return f"Giỏ hàng của {self.cart_customer.username}: {self.cart_product.prod_name}"
    
    # Một khách hàng không thể thêm trùng món ăn vào giỏ
    class Meta:
        unique_together = ('cart_customer', 'cart_product')  

    # Tính tổng tiền cho 1 món ăn nếu được chọn
    @property
    def get_total_cart(self):
        if self.is_selected:
            return self.cart_product.prod_price * self.cart_product_quantity
        return 0

    # Tính tổng tiền trong giỏ hàng
    @staticmethod
    def calculate_selected_total(user):
        # Lấy tất cả các mục trong giỏ hàng của người dùng và đã được chọn
        selected_items = Cart.objects.filter(cart_customer=user, is_selected=True)
        # Tính tổng tiền từ tất cả các mục
        total = sum(item.cart_product.prod_price * item.cart_product_quantity for item in selected_items)
        return total

# Đơn hàng: Gồm khách hàng, ngày đặt, tình trạng đơn hàng, tổng tiền, phương thức thanh toán, người nhận đơn, số điện thoại của họ, địa chỉ giao hàng
class Order(models.Model):
    UNIT_TYPE_CHOICES = [
        ('Đang xử lý', 'Đang xử lý'),
        ('Đang giao', 'Đang giao'),
        ('Đã giao', 'Đã giao'),
        ('Đã hủy', 'Đã hủy'),
    ]
    METHOD_CHOICE = [
        ('Thanh toán tiền mặt khi nhận hàng', 'Thanh toán tiền mặt khi nhận hàng'),
        ('Thanh toán bằng thẻ ATM nội địa và tài khoản ngân hàng', 'Thanh toán bằng thẻ ATM nội địa và tài khoản ngân hàng'),
    ]
    order_customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    order_date = models.DateField(auto_now_add=True)
    order_status = models.CharField(max_length=100,choices=UNIT_TYPE_CHOICES)
    order_total = models.IntegerField(null=True,blank=False)
    order_method = models.CharField(max_length=100,choices=METHOD_CHOICE)
    
    order_receiver_name = models.CharField(max_length=100,null=True,blank=False)
    order_receiver_phone = models.CharField(max_length=15,null=True,blank=False)
    order_adress = models.CharField(max_length=100,null=True,blank=False)

    def __str__(self) -> str:
        return f"Đơn hàng từ {self.order_customer} vào ngày {self.order_date}"
# CHi tiết đơn hàng: 1 đơn hàng có nhiều chi tiết đơn hàng, mỗi chi tiết đại diện cho 1 món ăn trong đơn và số lượng món ăn đó   
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False)
    quantity = models.IntegerField(null=True,blank=False)
    
    def __str__(self) -> str:
        return f"Đơn {self.order.order_customer} vào ngày {self.order.order_date} đặt {self.product.prod_name}"