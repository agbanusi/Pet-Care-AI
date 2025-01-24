from pony.orm import Required, Optional, Set
from .base import Base_Model

class Wallet(Base_Model):
    _table_ = 'wallets'
    # customer = Required('Customer')
    wallet_customer = Optional('Customer')
    wallet_vendor = Optional('Vendor')
    wallet_rider = Optional('Rider')
    wallet_balance = Required(float, default=0.0)
    wallet_transactions = Set('Transaction')