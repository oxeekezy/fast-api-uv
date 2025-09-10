from pydantic import EmailStr
from web.dao.base import BaseDAO
from web.users.models import Users


class UserDAO(BaseDAO):
    model = Users
    
    async def get_user_by_email(email: EmailStr) -> Users | None:
        result = await UserDAO.get_by_params(email=email)
        if result:
            return result[0]
        return None
    
        