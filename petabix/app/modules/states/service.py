from pony.orm import db_session
from models.state import State
from models.country import Country
from fastapi import HTTPException

class StateService:
    @db_session
    async def list_states(self, country_id: int):
        country = Country.get(id=country_id)
        if not country:
            raise HTTPException(status_code=404, detail="Country not found")
        return list(country.states)

    @db_session
    async def get_state(self, state_id: int):
        state = State.get(id=state_id)
        if not state:
            raise HTTPException(status_code=404, detail="State not found")
        return state