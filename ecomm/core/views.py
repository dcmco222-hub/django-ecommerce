from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import (Product, Category, Cart, CartItem, Order, OrderItem)
from django.db.models import Q

# Create your views here.


def home(request):
    products = Product.objects.filter(available=True).order_by("-created_at")[:12]
    categories = Category.objects.all()

    return render(request, "core/home.html", {
        "products": products,
        "categories": categories
    })


def product_list(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    return render(request, "core/product_list.html", {
        "products": products,
        "categories": categories
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(available=True)

    return render(request, "core/category_detail.html", {
        "category": category,
        "products": products
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)

    return render(request, "core/product_detail.html", {
        "product": product
    })



@login_required
def dashboard(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    available_products = Product.objects.filter(available=True).count()

    context = {
        "total_products": total_products,
        "total_categories": total_categories,
        "available_products": available_products,
    }

    return render(request, "core/dashboard.html", context)

# ===== ADD TO CART ===== #
@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")

# ===== VIEW CART ===== #
@login_required
def cart(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.all()

    total = sum(
        item.subtotal
        for item in items
    )

    return render(
        request,
        "core/cart.html",
        {
            "items": items,
            "total": total
        }
    )

# ===== REMOVE ITEM ===== #
@login_required
def remove_from_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id
    )

    item.delete()

    return redirect("cart")

# ===== Increase Quantity ===== #
@login_required
def increase_quantity(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id
    )

    item.quantity += 1
    item.save()

    return redirect("cart")

# ===== DECREASE QUANTITY ===== #
@login_required
def decrease_quantity(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart")

def category_list(request):

    categories = Category.objects.all()

    return render(
        request, "core/category_list.html", {"categories": categories}
    )

def search_products(request):

    query = request.GET.get("q", "")

    products = Product.objects.filter(
        available=True
    )

    if query:
        products = products.filter(
            name__icontains=query
        )

    category = request.GET.get("category")

    if category:
        products = products.filter(
            category__id=category
        )

    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if min_price:
        products = products.filter(
            price__gte=min_price
        )

    if max_price:
        products = products.filter(
            price__lte=max_price
        )

    stock = request.GET.get("stock")

    if stock == "in":
        products = products.filter(
            stock__gt=0
        )

    categories = Category.objects.all()

    return render(
        request,
        "core/search_results.html",
        {"products": products, "query": query, "categories": categories,}
    )



@login_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "core/order_success.html",
        {
            "order": order
        }
    )

@login_required
def checkout(request):

    cart, created = Cart.objects.get_or_create(
    user=request.user
    )

    items = cart.items.all()

    total = sum(
        item.subtotal
        for item in items
    )

    if request.method == "POST":

        order = Order.objects.create(
            user=request.user,
            total_price=total
        )

        for item in items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_final_price()
            )

        items.delete()

        return redirect(
            "order_success",
            order_id=order.id
        )

    return render(
        request,
        "core/checkout.html",
        {
            "items": items,
            "total": total
        }
    )