from sqladmin import ModelView
from web.courses.models import CourseModel
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
    
class CourseAdminView(ModelView, model=CourseModel):
    can_create=False
    can_delete=True
    name="Курс"
    name_plural="Курсы"
    column_list = [
        CourseModel.id,
        CourseModel.name,
        CourseModel.desc,
        CourseModel.duration,
        CourseModel.teacher
    ]
        
    