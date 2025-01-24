from pony.orm import Required, Optional, Set
from .base import Base_Model

class Transaction(Base_Model):
    _table_ = 'transactions'
    wallet = Required('Wallet')
    transaction_amount = Required(float)
    transaction_type = Required(str)  # e.g., 'deposit', 'withdrawal', 'payment'
    transaction_description = Optional(str)