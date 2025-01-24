from pony.orm import Required, Optional, Set
from .base import Base_Model

class Location(Base_Model):
    _table_ = 'locations'
    latitude = Required(float)
    longitude = Required(float)
    address = Required(str)
    location_user = Optional('User')  # Can be associated with a user (e.g., for delivery)