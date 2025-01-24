from pony.orm import Database, sql_debug
from .config import settings

db = Database()

def init_db():
    db.bind(provider='postgres', host=settings.DB_HOST, user=settings.DB_USER,
            password=settings.DB_PASSWORD, database=settings.DB_NAME)
    db.generate_mapping(create_tables=True)
    if settings.DEBUG:
        sql_debug(True)