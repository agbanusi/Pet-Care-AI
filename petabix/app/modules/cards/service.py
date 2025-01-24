from pony.orm import db_session
from models.card import Card
from models.customer import Customer
from schemas.card import CardCreate, CardUpdate
from fastapi import HTTPException

class CardService:
    @db_session
    async def create_card(self, card: CardCreate, current_user: dict):
        customer = Customer.get(user=current_user['id'])
        if not customer:
            raise HTTPException(status_code=403, detail="Only customers can add cards")
        new_card = Card(
            customer=customer,
            card_number=card.card_number,
            expiry_date=card.expiry_date,
            card_holder_name=card.card_holder_name
        )
        return new_card

    @db_session
    async def get_card(self, card_id: int, current_user: dict):
        card = Card.get(id=card_id)
        if not card or card.customer.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Card not found or unauthorized")
        return card

    @db_session
    async def list_cards(self, current_user: dict):
        customer = Customer.get(user=current_user['id'])
        return list(customer.cards)

    @db_session
    async def update_card(self, card_id: int, card_data: CardUpdate, current_user: dict):
        card = Card.get(id=card_id)
        if not card or card.customer.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Card not found or unauthorized")
        card.set(**card_data.dict(exclude_unset=True))
        return card

    @db_session
    async def delete_card(self, card_id: int, current_user: dict):
        card = Card.get(id=card_id)
        if not card or card.customer.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Card not found or unauthorized")
        card.delete()
        return True