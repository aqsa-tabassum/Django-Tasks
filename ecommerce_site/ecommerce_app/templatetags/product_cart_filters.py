from django import template
register = template.Library()


@register.filter(name = 'is_product_in_cart')
def is_product_in_cart(product, cart):
    added_product_ids = cart.keys()
    for added_product_id in added_product_ids:
        if product.id == int(added_product_id):
            return True
    return False


@register.filter(name = 'product_count_in_cart')
def product_count_in_cart(product, cart):
    added_product_ids = cart.keys()
    for added_product_id in added_product_ids:
        if product.id == int(added_product_id):
            return cart.get(added_product_id)
    return 0


@register.filter(name = 'cart_product_total_price')
def cart_product_total_price(product, cart):
    return product.price * product_count_in_cart(product, cart)


@register.filter(name = 'cart_total_bill')
def cart_total_bill(products, cart):
    total_bill_amount = 0;
    for product in products:
        total_bill_amount += cart_product_total_price(product, cart)
    return total_bill_amount