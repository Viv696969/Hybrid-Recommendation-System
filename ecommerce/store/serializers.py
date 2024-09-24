
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=["id","name","image_url","category","price"]
        depth=1

class CartSerializer(serializers.ModelSerializer):
    product_info=SerializerMethodField()
    class Meta:
        model=Cart
        fields=[
            'quantity',
            'total_price',
            'product_info',
        ]
        depth=1
    
    def get_product_info(self,cart):
        return {
            'name':cart.product.name,
            'id':cart.product.id,
            'price':cart.product.price,
        }
    