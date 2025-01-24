from pony.orm import Required, Optional, Set
from .base import Base_Model
from .user import UserPossess

class Like(UserPossess):
    _table_ = 'likes'
    liked_post = Required('Post')