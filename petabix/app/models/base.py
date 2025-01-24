from pony.orm import PrimaryKey, Required, Optional
from datetime import datetime
from core.database import db

class Base_Model(db.Entity):
    id = PrimaryKey(int, auto=True)
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Optional(datetime)