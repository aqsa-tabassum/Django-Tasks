from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from ecommerce_app.forms import *
from ecommerce_app.models import *
from django.contrib import messages


def home(request):
    """
    If user submit a search form, we have to search that product
    and pass in context to display filtered products.
    """
    if request.method == 'POST':
        if request.POST.get('product_input'):
            product_input = request.POST.get('product_input')
            filtered_product_object = Product.objects.filter(name=product_input)
            context = {
                'filtered_product': filtered_product_object
            }
            return render(request, 'products/crud/search_product.html', context)
        """
        Getting product id in order to initialize cart if does not exit, and 
        to increase, decrease quantity of product in cart if products exist 
        in cart.
         """
        if request.POST.get('product_id'):
            product_id = request.POST.get('product_id')
            product_obj = Product.objects.get(id=product_id)
            is_product_removed = request.POST.get('is_product_removed')
            cart = request.session.get('cart')
            if cart:
                quantity = cart.get(product_id)
                if quantity:
                    if is_product_removed:
                        if quantity == 1:
                            cart.pop(product_id)
                        else:
                            cart[product_id] = quantity - 1
                            product_obj.inventory_count += 1
                            product_obj.save()
                    else:
                        cart[product_id] = quantity + 1
                        product_obj.inventory_count -= 1
                        product_obj.save()
                else:
                    cart[product_id] = 1
                    product_obj.inventory_count -= 1
                    product_obj.save()
            else:
                cart = {}
                cart[product_id] = 1
                product_obj.inventory_count -= 1
                product_obj.save()

            request.session['cart'] = cart
            return redirect('/')
    """
    Passing all products that will display on home page and categories
    for tabs in home page.
    """
    products = Product.objects.all()
    product_categories = Product.objects.order_by().values_list\
        ('category__category', flat=True).distinct()

    """
    Passing unseen number of requests to be shown to admin
    """
    unseen_requests = CustomerProductRequest.objects.filter(request_seen=False).count()
    context = {
        'new_product_requests_count': unseen_requests,
        'products': products,
        'categories': product_categories
    }
    return render(request, 'index.html', context)


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            products = Product.objects.all()
            context = {
                'products': products,
            }
            return render(request, 'products/crud/all_products.html', context)
    else:
        form = ProductForm()
    return render(request, 'products/crud/product_form.html', {'form': form})


def create_category_popup(request):
    form = ProductCategoryForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_category");</script>' % (instance.pk, instance))
    return render(request, "products/crud/category_form.html", {"form": form})


def edit_category_popup(request, pk=None):
    instance = get_object_or_404(ProductCategory, pk=pk)
    form = ProductCategoryForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_category");</script>' % (instance.pk, instance))
    return render(request, "products/crud/category_form.html", {"form": form})


@csrf_exempt
def get_category_id(request):
    if request.is_ajax():
        category = request.GET['category_name']
        category_id = ProductCategory.objects.get(category=category).id
        data = {'category_id': category_id, }
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


def update_product(request, id):
    context = {}
    obj = get_object_or_404(Product, id = id)
    form = ProductForm(request.POST or None, request.FILES or None, instance = obj)
    if form.is_valid():
        form.save()
        return redirect("ecommerce_app:all_products")
    context["form"] = form
    return render(request, "products/crud/update_product.html", context)


def delete_product(request, pk):
    if request.method == "POST":
        product = Product.objects.get(pk=pk)
        product.delete()
    return redirect("ecommerce_app:all_products")


def all_products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products/crud/all_products.html', context)


def category_wise_products(request, category):
    products_by_category = Product.objects.filter(category__category=category)
    category_name = category
    category_heading = "{}{}".format(category_name, " Product Category")

    # Passing Products Categories for tabs
    product_categories = Product.objects.order_by().values_list \
        ('category__category', flat=True).distinct()

    context = {
        'category_heading': category_heading,
        'products': products_by_category,
        'categories': product_categories,
    }
    return render(request, 'index.html', context)


def request_new_product(request):
    if request.method == 'POST':
        form = NewProductRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ecommerce_app:home')
    else:
        form = NewProductRequestForm()
    return render(request, 'products/product_requests/request_form.html', {'form': form})


def show_unseen_product_requests(request):
    unseen_products_requests = CustomerProductRequest.objects.filter(request_seen=False)
    context = {
        'unseen_products_requests': unseen_products_requests,
    }
    return render(request, 'products/product_requests/all_requested_products.html', context)


def mark_requests_as_read(request):
    CustomerProductRequest.objects.filter(request_seen=False).update(request_seen = True)
    return redirect('ecommerce_app:home')


def user_cart(request):
    if request.session.get('cart'):
        product_ids_in_cart = list(request.session.get('cart').keys())
        products_in_cart = Product.get_products_by_id(product_ids_in_cart)
        context = {
            'products_in_cart': products_in_cart,
        }
        return render(request, 'cart/cart_products.html', context)
    else:
        messages.error(request, "Your Cart is empty. Add products in cart to view.")
        return redirect("ecommerce_app:home")