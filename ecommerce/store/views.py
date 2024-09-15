from django.shortcuts import render
from authentication.models import Profile
from rest_framework.decorators import api_view,permission_classes
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import *
from django.http import JsonResponse
from rest_framework.status import *
from .serializers import ProductSerializer,CartSerializer
from rest_framework.permissions import IsAuthenticated
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
        if 'activity' in request.data:
            data=request.data
            resp=requests.post("http://127.0.0.1:8888/recommend_by_activity",json=data)
            ids=list(map(int ,resp.json()['data']))
            products=Product.objects.filter(id__in=ids)
            products=sorted(products,key=lambda x: ids.index(x.id))
            data=ProductSerializer(products,many=True).data
            return JsonResponse(data=data,status=200,safe=False)
        else:
            products=Product.objects.all()
            data=ProductSerializer(products,many=True).data
            return JsonResponse(data=data,status=HTTP_200_OK,safe=False)
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


@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def show_product(request):
    product_id=request.POST['product_id']
    product=Product.objects.get(id=int(product_id))
    resp=requests.post("http://127.0.0.1:8888/recommend_products",json={'product_id':product_id})
    ids=list(map(int,resp.json()['data']))
    products=sorted(Product.objects.filter(id__in=ids),key=lambda x: ids.index(x.id))
    return JsonResponse(
        {
            'product':ProductSerializer(product).data,
            'recommended_products':ProductSerializer(products,many=True).data
        },
        status=200,
        safe=False
    )

@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    try:
        product_id=request.POST['product_id']
        product=Product.objects.get(id=product_id)
        user=request.user
        cart=Cart.objects.create(product=product,user=user,total_price=product.price)
        cart.save()
        return JsonResponse({
            'status':True,'mssg':f'{product.name} added to cart..'
        },status=200)
    except:
        return JsonResponse({
            'status':False,'mssg':f'Product Not found'
        },status=404)
    
@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    cart_size=len(cart)
    if cart_size>0:
        data=CartSerializer(cart,many=True).data
        return JsonResponse({
            'quantity':cart_size,
            'data':data,
            'status':True
        },status=200)

    else:
        return JsonResponse({
            'status':False,
            'mssg':'No items in Cart..'
        })
    
@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def place_order(request):
    carts=Cart.objects.filter(user=request.user)
    order=Order.objects.create(
        user=request.user
    )
    total_price=0
    profile=Profile.objects.get(user=request.user)
    for cart in carts:
        total_price+=cart.total_price
        ordered_item=OrderItem.objects.create(
            order=order,product=cart.product,total_price=cart.total_price
            )
        profile.add_item_id(cart.product.id)
        ordered_item.save()
        cart.delete()
        
    profile.save()
    order.save()
    return JsonResponse({
        'mssg':'Order Placed successffully!!',
        'order_id':order.id
    },status=201)