from pony.orm import Required, Optional, Set
from .base import Base_Model
from .user import User, UserPossess

class Customer(UserPossess):
    _table_ = 'customers'
    full_name = Required(str)
    customer_phone = Required(str)
    customer_address = Required(str)
    customer_orders = Set('Order')
    customer_appointments = Set('Appointment')
    customer_reviews = Set('Review')
    customer_cart = Optional('Cart')
    customer_wallet = Optional('Wallet')