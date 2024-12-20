# Generated by Django 5.0.10 on 2024-12-14 08:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category_lv1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cate_1', models.CharField(choices=[('Khai vị', 'Khai vị'), ('Món chính', 'Món chính'), ('Món tráng miệng', 'Món tráng miệng'), ('Nước uống', 'Nước uống')], max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Category_lv2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cate_2', models.CharField(max_length=500)),
                ('cate_2_image', models.ImageField(null=True, upload_to='')),
                ('num_products', models.IntegerField(default=0)),
                ('cate_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category_lv1')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(auto_now_add=True)),
                ('order_status', models.CharField(choices=[('Đang xử lý', 'Đang xử lý'), ('Đang giao', 'Đang giao'), ('Đã giao', 'Đã giao'), ('Đã hủy', 'Đã hủy')], max_length=100)),
                ('order_total', models.IntegerField(null=True)),
                ('order_method', models.CharField(choices=[('Thanh toán tiền mặt khi nhận hàng', 'Thanh toán tiền mặt khi nhận hàng'), ('Thanh toán bằng thẻ ATM nội địa và tài khoản ngân hàng', 'Thanh toán bằng thẻ ATM nội địa và tài khoản ngân hàng')], max_length=100)),
                ('order_receiver_name', models.CharField(max_length=100, null=True)),
                ('order_receiver_phone', models.CharField(max_length=15, null=True)),
                ('order_adress', models.CharField(max_length=100, null=True)),
                ('order_customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_name', models.CharField(max_length=500)),
                ('prod_price', models.IntegerField()),
                ('prod_description', models.CharField(max_length=500, null=True)),
                ('prod_cate_lv1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category_lv1')),
                ('prod_cate_lv2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category_lv2')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(null=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='Product_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_image', models.ImageField(null=True, upload_to='')),
                ('is_avatar', models.BooleanField(default=False)),
                ('prod_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_product_quantity', models.IntegerField(default=1)),
                ('is_selected', models.BooleanField(default=False)),
                ('cart_customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('cart_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
            ],
            options={
                'unique_together': {('cart_customer', 'cart_product')},
            },
        ),
    ]
