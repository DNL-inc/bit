from gino import Gino
from data import config

db = Gino()

async def create_db():
    await db.set_bind(config.DB_URI)
    # await db.gino.drop_all()
    await db.gino.create_all()      
    

async def close_db():
    await db.pop_bind().close()