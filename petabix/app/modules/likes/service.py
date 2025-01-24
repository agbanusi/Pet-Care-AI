from pony.orm import db_session
from models.like import Like
from models.post import Post
from models.user import User
from schemas.like import LikeCreate
from fastapi import HTTPException

class LikeService:
    @db_session
    async def create_like(self, like: LikeCreate, current_user: dict):
        user = User.get(id=current_user['id'])
        post = Post.get(id=like.post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        existing_like = Like.get(user=user, post=post)
        if existing_like:
            raise HTTPException(status_code=400, detail="Already liked")
        new_like = Like(user=user, post=post)
        return new_like

    @db_session
    async def get_likes_for_post(self, post_id: int):
        post = Post.get(id=post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return list(post.likes)

    @db_session
    async def remove_like(self, post_id: int, current_user: dict):
        user = User.get(id=current_user['id'])
        post = Post.get(id=post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        like = Like.get(user=user, post=post)
        if not like:
            raise HTTPException(status_code=404, detail="Like not found")
        like.delete()
        return True