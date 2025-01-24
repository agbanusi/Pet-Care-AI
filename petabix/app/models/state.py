from pony.orm import Required, Optional, Set
from .base import Base_Model

class State(Base_Model):
    _table_ = 'states'
    state_name = Required(str)
    state_code = Required(str)
    country = Required('Country')