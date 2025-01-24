from pony.orm import Required, Optional, Set
from .base import Base_Model

class Card(Base_Model):
    _table_ = 'cards'
    card_customer = Required('Customer')
    card_number = Required(str)
    card_expiry_date = Required(str)
    card_holder_name = Required(str)