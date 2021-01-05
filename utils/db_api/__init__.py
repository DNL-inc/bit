from gino import Gino
from data import config

db = Gino()

async def create_db():
    await db.set_bind(config.DB_URI)
    
async def close_db():
    await db.pop_bind().close()