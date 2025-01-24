from pony.orm import Required, Optional, Set
from .base import Base_Model
from .user import User, UserPossess

class Rider(UserPossess):
    _table_ = 'riders'
    # user = Required(User)
    vehicle_type = Required(str)
    license_plate = Required(str, unique=True)
    rider_orders = Set('Order')