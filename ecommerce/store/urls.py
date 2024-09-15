from django.urls import path
from .views import *

urlpatterns = [
    path("add_product",add_product,name="add_product"),
    path("show_products",show_products,name="show_products"),
    path("send_products",send_products,name="send_products"),
]