from tortoise import Tortoise
from data import config


async def init_db():
    db = await Tortoise.init(
        db_url=config.DB_URI,
        modules={'models': ['models', 'aerich.models']}
    )    
    return db
