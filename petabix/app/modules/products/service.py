from pony.orm import db_session
from models.product import Product
from models.vendor import Vendor
from schemas.product import ProductCreate, ProductUpdate
from fastapi import HTTPException

class ProductService:
    @db_session
    async def create_product(self, product: ProductCreate, current_user: dict):
        vendor = Vendor.get(user=current_user['id'])
        if not vendor:
            raise HTTPException(status_code=403, detail="Only vendors can create products")
        new_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            category=product.category,
            vendor=vendor
        )
        return new_product

    @db_session
    async def get_product(self, product_id: int):
        product = Product.get(id=product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    @db_session
    async def list_products(self, skip: int, limit: int):
        return list(Product.select().offset(skip).limit(limit))

    @db_session
    async def update_product(self, product_id: int, product_data: ProductUpdate, current_user: dict):
        product = Product.get(id=product_id)
        if not product or product.vendor.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Product not found or unauthorized")
        product.set(**product_data.dict(exclude_unset=True))
        return product

    @db_session
    async def delete_product(self, product_id: int, current_user: dict):
        product = Product.get(id=product_id)
        if not product or product.vendor.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Product not found or unauthorized")
        product.delete()
        return True
