from pony.orm import Required, Optional, Set
from .base import Base_Model

class User(Base_Model):
    # _table_ = 'users'
    username = Required(str, unique=True)
    email = Required(str, unique=True)
    hashed_password = Required(str)
    is_active = Required(bool, default=True)
    is_superuser = Required(bool, default=False)
    # customer = Optional('Customer')
    # vendor = Optional('Vendor')
    # veterinarian = Optional('Veterinarian')
    # rider = Optional('Rider')
    posts = Set('Post')
    comments = Set('Comment')
    likes = Set('Like')
    location = Set('Location')

class UserPossess(User):
    # user = Required(User)
    pass