from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),

    path(
        'register/buyer/',
        views.buyer_register,
        name='buyer_register'
    ),

    path(
        'register/seller/',
        views.seller_register,
        name='seller_register'
    ),
]
