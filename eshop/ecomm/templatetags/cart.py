from django import template
from numpy import product

register = template.Library()


@register.filter(name="isExistsInCart")
def isExistsInCart(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False


@register.filter(name="cartQunat")
def cartQunat(product, cart):

    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0


@register.filter(name="prod_total")
def prod_total(product, cart):
    return product.price * cartQunat(product, cart)


@register.filter(name="total_price")
def total_price(product, cart):
    sum = 0
    for tp in product:
        sum += prod_total(tp, cart)
    return sum
