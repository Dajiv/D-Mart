
from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path("my_orders/", views.my_orders_view, name="my_orders"),
    path("<int:order_id>/cancel/",views.cancel_order_view, name="cancel_order"),

    
]