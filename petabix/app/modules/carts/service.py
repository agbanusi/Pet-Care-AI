from pony.orm import db_session
from models.cart import Cart, CartItem
from models.customer import Customer
from models.product import Product
from schemas.cart import CartItemCreate, CartItemUpdate
from fastapi import HTTPException

class CartService:
    @db_session
    async def add_to_cart(self, item: CartItemCreate, current_user: dict):
        customer = Customer.get(user=current_user['id'])
        product = Product.get(id=item.product_id)
        
        if not customer or not product:
            raise HTTPException(status_code=400, detail="Invalid customer or product")
        
        cart = customer.cart or Cart(customer=customer)
        cart_item = CartItem(cart=cart, product=product, quantity=item.quantity)
        return cart

    @db_session
    async def get_cart(self, current_user: dict):
        customer = Customer.get(user=current_user['id'])
        return customer.cart

    @db_session
    async def update_cart_item(self, item_id: int, item_data: CartItemUpdate, current_user: dict):
        customer = Customer.get(user=current_user['id'])
        cart_item = CartItem.get(id=item_id, cart=customer.cart)
        
        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        
        cart_item.quantity = item_data.quantity
        return customer.cart

    @db_session
    async def remove_from_cart(self, item_id: int, current_user: dict):
        customer = Customer.get(user=current_user['id'])
        cart_item = CartItem.get(id=item_id, cart=customer.cart)
        
        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        
        cart_item.delete()
        return customer.cart