
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from products.models import Cart


@login_required
def checkout_view(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = list(
        cart.items.select_related(
            "product",
            "product__seller"
        )
    )

    if not cart_items:
        messages.error(
            request,
            "Your cart is empty. Please add a product first."
        )
        return redirect("cart")

    valid_items = []
    subtotal = Decimal("0.00")

    for item in cart_items:
        product = item.product

        if product.status != "ACTIVE":
            messages.error(
                request,
                f"{product.name} is not available right now."
            )
            return redirect("cart")

        if product.stock <= 0:
            messages.error(
                request,
                f"{product.name} is out of stock."
            )
            return redirect("cart")

        if item.quantity > product.stock:
            messages.error(
                request,
                f"Only {product.stock} units of {product.name} are available."
            )
            return redirect("cart")

        item.subtotal = product.price * item.quantity
        subtotal += item.subtotal
        valid_items.append(item)

    delivery_fee = Decimal("0.00")
    grand_total = subtotal + delivery_fee

    context = {
        "valid_items": valid_items,
        "cart_items": valid_items,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "grand_total": grand_total,
        "default_name": request.user.get_full_name()
        or request.user.username,
    }

    return render(
        request,
        "orders/checkout.html",
        context
    )
