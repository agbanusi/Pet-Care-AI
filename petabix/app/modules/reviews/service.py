from pony.orm import db_session
from models.review import Review
from models.product import Product
from models.customer import Customer
from schemas.review import ReviewCreate, ReviewUpdate
from fastapi import HTTPException

class ReviewService:
    @db_session
    async def create_review(self, review: ReviewCreate, current_user: dict):
        customer = Customer.get(user=current_user['id'])
        product = Product.get(id=review.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        new_review = Review(
            customer=customer,
            product=product,
            rating=review.rating,
            comment=review.comment
        )
        return new_review

    @db_session
    async def get_review(self, review_id: int):
        review = Review.get(id=review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return review

    @db_session
    async def get_reviews_for_product(self, product_id: int):
        product = Product.get(id=product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return list(product.reviews)

    @db_session
    async def update_review(self, review_id: int, review_data: ReviewUpdate, current_user: dict):
        review = Review.get(id=review_id)
        if not review or review.customer.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Review not found or unauthorized")
        review.set(**review_data.dict(exclude_unset=True))
        return review

    @db_session
    async def delete_review(self, review_id: int, current_user: dict):
        review = Review.get(id=review_id)
        if not review or review.customer.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Review not found or unauthorized")
        review.delete()
        return True
