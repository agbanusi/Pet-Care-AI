from pony.orm import Required, Optional, Set
from .base import Base_Model
from .vendor import Vendor

class Product(Base_Model):
    _table_ = 'products'
    product_name = Required(str)
    product_description = Required(str)
    product_price = Required(float)
    product_available = Required(int)
    product_vendor = Set(Vendor)
    product_category = Required(str)
    product_reviews = Set('Review')
    product_order_items = Set('OrderItem')