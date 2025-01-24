from pony.orm import db_session
from models.comment import Comment
from models.post import Post
from models.user import User
from schemas.comment import CommentCreate, CommentUpdate
from fastapi import HTTPException

class CommentService:
    @db_session
    async def create_comment(self, comment: CommentCreate, current_user: dict):
        user = User.get(id=current_user['id'])
        post = Post.get(id=comment.post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        new_comment = Comment(user=user, post=post, content=comment.content)
        return new_comment

    @db_session
    async def get_comment(self, comment_id: int):
        comment = Comment.get(id=comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment

    @db_session
    async def get_comments_for_post(self, post_id: int):
        post = Post.get(id=post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return list(post.comments)

    @db_session
    async def update_comment(self, comment_id: int, comment_data: CommentUpdate, current_user: dict):
        comment = Comment.get(id=comment_id)
        if not comment or comment.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Comment not found or unauthorized")
        comment.content = comment_data.content
        return comment

    @db_session
    async def delete_comment(self, comment_id: int, current_user: dict):
        comment = Comment.get(id=comment_id)
        if not comment or comment.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Comment not found or unauthorized")
        comment.delete()
        return True