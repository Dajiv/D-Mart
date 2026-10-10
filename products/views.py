from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem
from decimal import Decimal
from django.views.decorators.http import require_POST
from django.contrib import messages

def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        status='ACTIVE'
    )

    return render(
        request,
        'products/product_detail.html',
        {
            'product': product
        }
    )


@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        status='ACTIVE'
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def cart_view(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = list(
        cart.items.select_related(
            'product',
            'product__seller'
        )
    )

    total_items_count = sum(
        item.quantity
        for item in cart_items
    )

    valid_items_count = 0
    cart_subtotal = Decimal('0.00')
    has_stock_issues = False

    for item in cart_items:

        product = item.product

        item.subtotal = (
            product.price * item.quantity
        )

        # Product inactive
        if product.status != 'ACTIVE':

            item.is_valid = False
            has_stock_issues = True

        # Product out of stock
        elif product.stock <= 0:

            item.is_valid = False
            has_stock_issues = True

        # Cart quantity greater than current stock
        elif item.quantity > product.stock:

            item.is_valid = False
            has_stock_issues = True

        # Valid item
        else:

            item.is_valid = True

            valid_items_count += 1

            cart_subtotal += item.subtotal

    can_checkout = (
        valid_items_count > 0
        and not has_stock_issues
    )

    return render(
        request,
        'products/cart.html',
        {
            'cart': cart,
            'cart_items': cart_items,
            'total_items_count': total_items_count,
            'valid_items_count': valid_items_count,
            'cart_subtotal': cart_subtotal,
            'has_stock_issues': has_stock_issues,
            'can_checkout': can_checkout,
        }
    )   

    
@login_required
def update_cart_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    product = cart_item.product

    if request.method == 'POST':

        action = request.POST.get('action')

        if action == 'increase':

            if (
                product.status == 'ACTIVE'
                and product.stock > 0
                and cart_item.quantity < product.stock
            ):
                cart_item.quantity += 1
                cart_item.save()

        elif action == 'decrease':

            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()

    return redirect('cart')

@login_required
@require_POST
def remove_cart_item(request, item_id):
    deleted_count, _ = CartItem.objects.filter(
        id=item_id,
        cart__user=request.user
    ).delete()

    if deleted_count:
        messages.success(request, "Product removed from your cart.")
    else:
        messages.error(request, "Cart item not found.")

    return redirect('cart')
