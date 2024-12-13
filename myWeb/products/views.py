from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def TrangChu(request):
    return render(request,"TrangChu.html")