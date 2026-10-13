
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from products.models import Cart, Product
from .models import Order, OrderItem


@login_required
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        district = request.POST.get("district", "").strip()
        postal_code = request.POST.get("postal_code", "").strip()
        payment_method = request.POST.get("payment_method", "").strip()

        if not all([full_name, phone, address, district, postal_code]):
            messages.error(request, "Please complete all delivery details.")
            return redirect("checkout")

        if payment_method != "COD":
            messages.error(
                request,
                "Online payment is not available yet. Please select COD."
            )
            return redirect("checkout")

        try:
            with transaction.atomic():
                cart = get_object_or_404(
                    Cart.objects.select_for_update(),
                    user=request.user
                )

                cart_items = list(
                    cart.items.select_related("product", "product__seller")
                )

                if not cart_items:
                    messages.error(request, "Your cart is empty.")
                    return redirect("cart")

                checked_items = []
                subtotal = Decimal("0.00")

                # Lock and validate every product before creating the order.
                for item in cart_items:
                    product = Product.objects.select_for_update().get(
                        pk=item.product_id
                    )

                    if product.status != "ACTIVE":
                        raise ValueError(
                            f"{product.name} is no longer available."
                        )

                    if product.stock < item.quantity:
                        raise ValueError(
                            f"Insufficient stock for {product.name}. "
                            f"Available: {product.stock}."
                        )

                    item_subtotal = product.price * item.quantity
                    subtotal += item_subtotal
                    checked_items.append(
                        (product, item.quantity, item_subtotal)
                    )

                delivery_fee = Decimal("0.00")
                grand_total = subtotal + delivery_fee

                delivery_address = (
                    f"{full_name}\n{address}\n"
                    f"{district}\nPostal code: {postal_code}"
                )

                order = Order.objects.create(
                    user=request.user,
                    delivery_address=delivery_address,
                    phone=phone,
                    total_amount=grand_total,
                    payment_method="COD",
                    payment_status="PENDING",
                    status="PENDING",
                )

                for product, quantity, item_subtotal in checked_items:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        seller=product.seller,
                        product_name=product.name,
                        quantity=quantity,
                        unit_price=product.price,
                        subtotal=item_subtotal,
                    )

                    product.stock -= quantity
                    product.save(update_fields=["stock"])

                cart.items.all().delete()

            messages.success(
                request,
                f"Order #{order.id} placed successfully!"
            )
            return render(
                request,
                "orders/order_success.html",
                {"order": order}
            )

        except ValueError as error:
            messages.error(request, str(error))
            return redirect("cart")

    cart_items = list(
        cart.items.select_related("product", "product__seller")
    )

    if not cart_items:
        messages.error(request, "Your cart is empty. Please add a product first.")
        return redirect("cart")

    

    subtotal = Decimal("0.00")

    for item in cart_items:
        product = item.product

        if (
            product.status != "ACTIVE"
            or product.stock <= 0
            or item.quantity > product.stock
        ):
            messages.error(
                request,
                f"Please check the availability of {product.name} in your cart."
            )
            return redirect("cart")

        item.subtotal = product.price * item.quantity
        subtotal += item.subtotal

    
    delivery_fee = Decimal("0.00")





    return render(
        request,
        "orders/checkout.html",
        {
            "valid_items": cart_items,
            "cart_items": cart_items,
            "subtotal": subtotal,
            "delivery_fee": delivery_fee,
            "grand_total": subtotal + delivery_fee,
            "default_name": request.user.get_full_name()
            or request.user.username,
        },
    )



@login_required
def my_orders_view(request):
    # Current user-oda orders mattum retrieve pannuvom
    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related("items")
    )

    # Search by Order ID
    search_query = request.GET.get("q", "").strip()

    if search_query.isdigit():
        orders = orders.filter(id=int(search_query))
    elif search_query:
        orders = orders.none()

    # Filter by order status
    status_filter = request.GET.get("status", "").strip()

    valid_statuses = [
        "PENDING",
        "CONFIRMED",
        "PROCESSING",
        "SHIPPED",
        "DELIVERED",
        "CANCELLED",
    ]

    if status_filter in valid_statuses:
        orders = orders.filter(status=status_filter)
    else:
        status_filter = ""

    # Filter by payment status
    payment_filter = request.GET.get("payment_status", "").strip()

    valid_payment_statuses = [
        "PENDING",
        "PAID",
        "FAILED",
        "REFUNDED",
    ]

    if payment_filter in valid_payment_statuses:
        orders = orders.filter(payment_status=payment_filter)
    else:
        payment_filter = ""

    # Sort newest or oldest
    sort_by = request.GET.get("sort", "newest").strip()

    if sort_by == "oldest":
        orders = orders.order_by("created_at", "id")
    else:
        sort_by = "newest"
        orders = orders.order_by("-created_at", "-id")

    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders,
            "search_query": search_query,
            "status_filter": status_filter,
            "payment_filter": payment_filter,
            "sort_by": sort_by,
        },
    )




@login_required
def cancel_order_view(request, order_id):
    # Cancellation must use POST, not a normal GET link.
    if request.method != "POST":
        messages.error(request, "Invalid cancellation request.")
        return redirect("my_orders")

    try:
        with transaction.atomic():
            # Lock the order and verify that it belongs to this user.
            order = get_object_or_404(
                Order.objects.select_for_update(),
                id=order_id,
                user=request.user,
            )

            # Only pending orders can be cancelled.
            if order.status != "PENDING":
                messages.error(
                    request,
                    "Only pending orders can be cancelled."
                )
                return redirect("my_orders")

            # Lock products and restore the reserved stock.
            order_items = (
                OrderItem.objects
                .filter(order=order)
                .order_by("product_id", "id")
            )

            for item in order_items:
                product = Product.objects.select_for_update().get(
                    pk=item.product_id
                )

                product.stock += item.quantity
                product.save(update_fields=["stock"])

            # Update the status inside the same transaction.
            order.status = "CANCELLED"
            order.save(update_fields=["status", "updated_at"])

        messages.success(
            request,
            f"Order #{order.id} cancelled successfully. Stock has been restored."
        )

    except Order.DoesNotExist:
        messages.error(request, "Order not found.")

    return redirect("my_orders")
