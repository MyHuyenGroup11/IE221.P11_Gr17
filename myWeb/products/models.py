from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    """ 1. Class CreateUserForm kế thừa từ UserCreationForm để tạo form đăng ký mới với các trường theo ý muốn """
    class Meta:
        model = User 
        
        # Lấy các trường cần thiết để tạo form đăng ký       
        fields = ['username','email','first_name','last_name','password1','password2']
        
        #Truyền vào các form 1 số thuộc tính cần thiết#
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập tên đăng nhập'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập email',
                'required': 'required'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập tên',
                'required': 'required'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập họ',
                'required': 'required'
            }),
            
            #Không truyền thuộc tính này vào các 2 form nhập lại mật khẩu được nên dùng JS thay thế
            'password1': forms.PasswordInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập mật khẩu'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập lại mật khẩu'
            }),
        }
        
    def clean_email(self):
        """ Tạo thêm ràng buộc email các user không được trùng nhau khi tạo tài khoản mới """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already taken.')
        return email


class Category_lv1(models.Model): 
    """ 2. Class Category_lv1 chứa phân loại các món ăn theo cấp 1 (Tên phân loại bao gồm: Khai vị, Món chính, Món tráng miệng, Nước uống) """
    UNIT_TYPE_CHOICES = [
        ('Khai vị', 'Khai vị'),
        ('Món chính', 'Món chính'),
        ('Món tráng miệng', 'Món tráng miệng'),
        ('Nước uống', 'Nước uống'),
    ]
    cate_1 = models.CharField(max_length=500, choices=UNIT_TYPE_CHOICES) # Tên phân loại món ăn cấp 1
    
    def __str__(self) -> str:
        return self.cate_1


class Category_lv2(models.Model):
    """ 3. Class Category_lv2 chứa phân loại các món ăn theo cấp 2 dựa trên các phân loại cấp 1 """
    cate_1 = models.ForeignKey(Category_lv1, on_delete=models.SET_NULL, null=True, blank=False) # Khóa ngoại tham chiếu đến phân loại món ăn cấp 1
    cate_2 = models.CharField(max_length=500) # Tên phân loại món ăn cấp 2
    num_products = models.IntegerField(default=0) # Số loại món ăn thuộc phân loại cấp 2

    def __str__(self) -> str:
        return self.cate_2
    
    def update_num_products(self):
        """ Cập nhật số loại món ăn trong phân loại cấp 2 """  
        self.num_products = Product.objects.filter(prod_cate_lv2=self).count()
        self.save()

class Product(models.Model):
    """ 4. Class Product chứa thông tin về một món ăn """
    prod_name = models.CharField(max_length=500) # Tên món ăn
    prod_price = models.IntegerField() # Giá món ăn
    prod_cate_lv1 = models.ForeignKey(Category_lv1, on_delete=models.SET_NULL, null=True, blank=False) # Khóa ngoại tham chiếu đến phân loại món ăn cấp 1
    prod_cate_lv2 = models.ForeignKey(Category_lv2, on_delete=models.SET_NULL, null=True, blank=False) # Khóa ngoại tham chiếu đến phân loại món ăn cấp 2
    prod_description = models.CharField(max_length=500,null=True, blank=False) # Thông tin về món ăn

    def __str__(self) -> str:
        return self.prod_name
    
    def get_avatar_url(self):
        """Lấy url cho ảnh avatar"""
        avatar = Product_Image.objects.filter(product=self, is_avatar=True).first()
        return avatar.ImageURL if avatar else None
    
    def formatted_price(self):
        """ Trả về giá được định dạng xxx,xxx """
        return "{:,.0f}".format(self.prod_price)
    
    @staticmethod
    def sort_products(products, sort_order='default'):
        """ Input: Danh sách sản phẩm -> Output: Danh sách sản phẩm được sắp xếp """
        if sort_order == 'asc':
            return products.order_by('prod_price')  # Sắp xếp tăng dần
        elif sort_order == 'desc':
            return products.order_by('-prod_price')  # Sắp xếp giảm dần
        return products  
    
class Product_Image(models.Model):
    """ 5. Class Product_Image chứa các ảnh của 1 món ăn, 1 món ăn có thể có nhiều ảnh khác nhau, nhưng chỉ có 1 ảnh là avatar"""
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False) # Khóa ngoại tham chiếu đến món ăn
    prod_image = models.ImageField(null=True, blank=False) # Ảnh của món ăn
    is_avatar = models.BooleanField(default=False) # Thuộc tính xác đĩnh xem ảnh có là avatar của món ăn hay không (True: Có ; False: Không)

    def __str__(self):
        # Kiểm tra nếu có liên kết tới món ăn
        if self.prod_name:
            # Nếu là avatar thì trả về avatar + tên món ăn
            if self.is_avatar:
                return f"avatar_{self.product.prod_name}" 
            return self.product.prod_name  # Còn không thì chỉ tên món ăn
        return "Unknown Product Image"  # Dự phòng nếu không có món ăn nào
    
    # class Meta:
    #     # Ràng buộc 1 món ăn chỉ có thể có 1 ảnh là avatar
    #     unique_together = ('product', 'is_avatar')  

    @property
    def ImageURL(self):
        """Trả về url của ảnh của món ăn hoặc trống để ngừa crash"""
        try:
            url = self.prod_image.url
        except :
            url = ''
        return url

class Cart(models.Model):
    """ 6. Class Giỏ hàng chứa thông tin các sản phẩm trong giỏ hàng của 1 user """
    cart_customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False) # Khóa ngoại tham chiếu đến user
    cart_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False) # Khóa ngoại tham chiếu đến món ăn
    cart_product_quantity = models.IntegerField(default=1) # Số lượng của món ăn đó trong giỏ hàng
    is_selected = models.BooleanField(default=False)  # Trạng chọn chọn hoặc không của món ăn
    
    def __str__(self) -> str:
        return f"Giỏ hàng của {self.cart_customer.username}: {self.cart_product.prod_name}"
    
    class Meta:
        # Ràng buộc một khách hàng không thể thêm trùng món ăn vào giỏ
        unique_together = ('cart_customer', 'cart_product')  

    @property
    def get_total_cart(self):
        """ Tính tổng tiền cho 1 món ăn nếu được chọn """
        if self.is_selected:
            return self.cart_product.prod_price * self.cart_product_quantity
        return 0

    @staticmethod
    def calculate_selected_total(user):
        """ Tính tổng tiền cho tất món ăn được chọn trong giỏ hàng"""
        # Lấy tất cả các món ăn trong giỏ hàng của người dùng và đã được chọn
        selected_items = Cart.objects.filter(cart_customer=user, is_selected=True)
        # Tính tổng tiền từ tất cả các món ăn
        total = sum(item.cart_product.prod_price * item.cart_product_quantity for item in selected_items)
        return total

# Đơn hàng: Gồm khách hàng, ngày đặt, tình trạng đơn hàng, tổng tiền, phương thức thanh toán, người nhận đơn, số điện thoại của họ, địa chỉ giao hàng
class Order(models.Model):
    """ 7. Class Order lưu trữ thông tin về một lần đặt món của user """
    
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
    order_customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)  # Khóa ngoại tham chiếu đến user
    order_date = models.DateField(auto_now_add=True) # Ngày đặt món, được cập nhật tự động
    order_status = models.CharField(max_length=100,choices=UNIT_TYPE_CHOICES) # Tình trạng đơn hàng: Đang xử lý, Đang giao, Đã giao, hoặc Đã hủy 
    order_total = models.IntegerField(null=True,blank=False) # Tổng giá tiền của đơn hàng
    order_method = models.CharField(max_length=100,choices=METHOD_CHOICE) # Phương thức thanh toán cho đơn hàng: Thanh toán tiền mặt khi nhận hàng, hoặc Thanh toán bằng thẻ ATM nội địa và tài khoản ngân hàng
    
    order_receiver_name = models.CharField(max_length=100,null=True,blank=False) # Tên người nhận hàng 
    order_receiver_phone = models.CharField(max_length=15,null=True,blank=False) # Số điện thoại người nhận hàng
    order_adress = models.CharField(max_length=100,null=True,blank=False) # Địa chỉ nhận hàng

    def __str__(self) -> str:
        return f"Đơn hàng từ {self.order_customer} vào ngày {self.order_date}"
 
class OrderItem(models.Model):
    """ 8. Class OrderItem chứa 1 thông tin về 1 món ăn trong 1 đơn hàng, 1 đơn hàng có thể có nhiều chi tiết đơn hàng """
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=False) # Khóa ngoại tham chiếu đế đơn hàng
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False) # Khóa ngoại tham chiếu đến món ăn
    quantity = models.IntegerField(null=True,blank=False) # Số lượng của món ăn trong chi tiết đơn hàng này
    
    def __str__(self) -> str:
        return f"Đơn {self.order.order_customer} vào ngày {self.order.order_date} đặt {self.product.prod_name}"