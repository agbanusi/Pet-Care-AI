from pony.orm import Required, Optional, Set
from .base import Base_Model
from .user import UserPossess

class Post(UserPossess):
    _table_ = 'posts'
    post_content = Required(str)
    post_likes = Set('Like')
    post_comments = Set('Comment')