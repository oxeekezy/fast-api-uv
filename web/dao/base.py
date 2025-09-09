from sqlalchemy import select, insert, delete

from web.database import ASYNC_SESSION_MAKER

class BaseDAO:
    model = None
    
    @classmethod
    async def get_all(cls):
        async with ASYNC_SESSION_MAKER() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()
            

    @classmethod
    async def get_by_id(cls, model_id: int):
        async with ASYNC_SESSION_MAKER() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalars().one_or_none()
        
    
    @classmethod
    async def add(cls, **data):
        async with ASYNC_SESSION_MAKER() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
            
    
    @classmethod
    async def delete(cls, user_id):
        async with ASYNC_SESSION_MAKER() as session:
            query = delete(cls.model).where(cls.model.id==user_id)
            await session.execute(query)
            await session.commit()
            
        
