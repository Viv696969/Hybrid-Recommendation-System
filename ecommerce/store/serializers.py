
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"
        depth=1