from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product
# Create your views here.


def say_Hello(request):
    # return HttpResponse('Hello World')
    #query_set = Product.objects.all()
   # query_set = Product.objects.filter(unit_price__gt=20)
    """for product in query_set:
        print(product)"""
    return render(request, 'hello.html', {'name': 'Uzaif'})  # 'products': list(query_set)})
