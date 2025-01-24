from pony.orm import Required, Optional, Set
from .base import Base_Model
from .user import User, UserPossess


class Vendor(UserPossess):
    _table_ = 'vendors'
    # user = Required(User)
    business_name = Required(str)
    business_address = Required(str)
    business_phone = Required(str)
    vendor_products = Set('Product')
    vendor_orders = Set('Order')