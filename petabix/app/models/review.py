from pony.orm import Required, Optional, Set
from .base import Base_Model

class Review(Base_Model):
    _table_ = 'reviews'
    review_customer = Required('Customer')
    review_product = Required('Product')
    review_rating = Required(int)
    review_comment = Optional(str)