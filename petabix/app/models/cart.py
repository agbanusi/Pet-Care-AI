from pony.orm import Required, Optional, Set
from .base import Base_Model

class CartItem(Base_Model):
    _table_ = 'cart_items'
    cart = Required('Cart')
    product = Required('Product')
    quantity = Required(int)

class Cart(Base_Model):
    _table_ = 'carts'
    cart_customer = Required('Customer')
    cart_items = Set('CartItem')