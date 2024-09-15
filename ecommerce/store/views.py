from django.shortcuts import render
from authentication.models import Profile
from rest_framework.decorators import api_view,permission_classes
import requests
from .models import *
from django.http import JsonResponse
from rest_framework.status import *
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