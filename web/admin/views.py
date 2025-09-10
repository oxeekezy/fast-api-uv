from sqladmin import ModelView
from web.users.models import UserModel

class UsersAdminView(ModelView, model=UserModel):
    can_create = False
    can_delete = True
    name = "Пользователь"
    name_plural = "Пользователи"
    column_list = [
        UserModel.id,
        UserModel.firstname,
        UserModel.lastname,
        UserModel.middlename,
        UserModel.email,
        UserModel.login
    ]
    column_details_exclude_list = [
        UserModel.password
    ]
        
    