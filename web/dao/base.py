from sqlalchemy import select, insert, delete

from web.database import ASYNC_SESSION_MAKER as sesson

class BaseDao:
    model = None
    
    @classmethod
    async def get_by_id(cls, model_id: int):
        async with sesson() as db:
            query = select(cls.model).filter_by(id=model_id)
            result = await db.execute(query)
            return result
    
    @classmethod
    async def add(cls, **kwargs):
        async with sesson() as db:
            query = insert(cls.model).values(**kwargs)
            await db.execute(query)
            await db.commit()
            
        
