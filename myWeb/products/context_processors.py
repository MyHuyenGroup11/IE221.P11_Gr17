from .models import *

def nav_categories(request):
    # Lấy danh mục cấp 1 và các danh mục cấp 2 liên quan
    categories_data = []
    categories_lv1 = Category_lv1.objects.all()

    for cate_lv1 in categories_lv1:
        categories_lv2 = Category_lv2.objects.filter(cate_1=cate_lv1)
        categories_data.append({
            "cate_lv1": cate_lv1,
            "categories_lv2": categories_lv2
        })

    return {
        "categories_data": categories_data
    }