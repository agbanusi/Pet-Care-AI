from pony.orm import Required, Optional, Set
from .base import Base_Model

class Country(Base_Model):
    _table_ = 'countries'
    country_name = Required(str, unique=True)
    country_code = Required(str, unique=True)
    states = Set('State')