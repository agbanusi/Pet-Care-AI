from pony.orm import Required, Optional, Set
from .base import Base_Model
from .user import UserPossess

class Comment(UserPossess):
    _table_ = 'comments'
    commented_post = Required('Post')
    comment = Required(str)