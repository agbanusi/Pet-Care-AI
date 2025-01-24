from pony.orm import Required, Optional, Set
from .base import Base_Model

class Order(Base_Model):
    _table_ = 'orders'
    order_customer = Required('Customer')
    order_vendor = Required('Vendor')
    order_rider = Optional('Rider')
    order_status = Required(str)  # e.g., 'pending', 'shipped', 'delivered'
    total_amount = Required(float)
    order_items = Set('OrderItem')

class OrderItem(Base_Model):
    _table_ = 'order_items'
    order = Required(Order)
    order_product = Required('Product')
    order_quantity = Required(int)
    order_price = Required(float)