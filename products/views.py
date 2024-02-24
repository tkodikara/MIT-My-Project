from django.shortcuts import render

# Create your views here.


def detail(request):
    return render(request, "products/products.html", {"products": "cool"})

