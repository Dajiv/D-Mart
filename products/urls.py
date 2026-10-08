from django.urls import path
from . import views


urlpatterns = [

    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'cart/add/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
    'cart/update/<int:item_id>/',
    views.update_cart_quantity,
    name='update_cart_quantity'
    ),

    path(
        'cart/',
        views.cart_view,
        name='cart'
    ),

]