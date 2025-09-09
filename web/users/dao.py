from web.dao.base import BaseDAO
from web.users.models import Users


class UserDAO(BaseDAO):
    model = Users