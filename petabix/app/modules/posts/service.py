from pony.orm import db_session
from models.post import Post
from models.user import User
from schemas.post import PostCreate, PostUpdate
from fastapi import HTTPException

class PostService:
    @db_session
    async def create_post(self, post: PostCreate, current_user: dict):
        user = User.get(id=current_user['id'])
        new_post = Post(user=user, content=post.content)
        return new_post

    @db_session
    async def get_post(self, post_id: int):
        post = Post.get(id=post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    @db_session
    async def list_posts(self, skip: int, limit: int):
        return list(Post.select().order_by(Post.created_at.desc()).offset(skip).limit(limit))

    @db_session
    async def update_post(self, post_id: int, post_data: PostUpdate, current_user: dict):
        post = Post.get(id=post_id)
        if not post or post.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Post not found or unauthorized")
        post.content = post_data.content
        return post

    @db_session
    async def delete_post(self, post_id: int, current_user: dict):
        post = Post.get(id=post_id)
        if not post or post.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Post not found or unauthorized")
        post.delete()
        return True
