from django.shortcuts import render
from authentication.models import Profile
from rest_framework.decorators import api_view,permission_classes
import requests
from .models import *
from django.http import JsonResponse
from rest_framework.status import *
from .serializers import ProductSerializer
import json
# Create your views here.


@api_view(['GET'])
def add_product(request):
    # try:
    url="https://fakestoreapi.com/products"
    resp=requests.get(url)
    data=resp.json()
    for item in data:
        category=Category.objects.filter(name=item['category']).first()
        description=item['description']
        product=Product.objects.create(
            category=category,
            description=description,
            name=item['title'],
            image_url=item['image'],
            price=item['price']
        )
        product.save()
        print("=========== Done ===============")

    return JsonResponse(data={
        'status':True
    },status=201)
    # except:
    #     return JsonResponse(data={'status':True},status=HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def show_products(request):
    print(request.user)
    user=request.user
    if user.is_authenticated:
        pass
    else:
        products=Product.objects.all()
        data=ProductSerializer(products,many=True).data
        return JsonResponse(data=data,status=HTTP_200_OK,safe=False)
    

@api_view(['GET']) 
def send_products(request):
    products=Product.objects.all()
    data=ProductSerializer(products,many=True).data
    resp=requests.post(
        "http://127.0.0.1:8888/add_product_to_vector",
        json=data
        )
    print(resp.status_code)
    return JsonResponse({'data':'ok'})