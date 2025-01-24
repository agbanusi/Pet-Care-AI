from pony.orm import Required, Optional, Set
from .base import Base_Model
from .user import User, UserPossess


class Veterinarian(UserPossess):
    _table_ = 'veterinarians'
    # user = Required(User)
    specialization = Required(str)
    license_number = Required(str, unique=True)
    appointments = Set('Appointment')