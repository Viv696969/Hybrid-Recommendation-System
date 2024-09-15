from django.urls import path
from .views import *

urlpatterns = [
    path("add_product",add_product,name="add_product"),
    path("show_products",show_products,name="show_products"),
    path("send_products",send_products,name="send_products"),
    path("show_product",show_product,name="show_product"),
    path("show_cart",show_cart,name="show_cart"),
    path("add_to_cart",add_to_cart,name="add_to_cart"),
    path("place_order",place_order,name="place_order"),
]