# from pydantic import BaseModel, EmailStr, field_validator
# from typing import Optional
# from datetime import datetime
# from dateutil.relativedelta import relativedelta


# class User(BaseModel):
#     """
#     Класс пользователя приложения
#     """
#     # id: int
#     firstname: str
#     lastname: str
#     middlename: Optional[str]
#     email: Optional[EmailStr]
#     age: Optional[int]
#     tel: Optional[RussianPhoneNumber]
#     birthday: datetime

#     login: str
#     reg_date: Optional[datetime]

#     @field_validator("login")
#     @classmethod
#     def login_validator(cls, value: str):
#         """
#         Валидация логина пользователя

#         Returns: str: Логин пользователя в lowercase
#         """
#         return value.lower()

#     @field_validator("tel", mode="before")
#     @classmethod
#     def phone_validator(cls, value: str):
#         """
#         Валидация логина пользователя

#         Returns: str: Логин пользователя в lowercase
#         """
#         if not value:
#             return None

#         if value.startswith("8"):
#             value = value.replace("8", "+7", 1)

#         return value

#     @field_validator("birthday")
#     @classmethod
#     def birthday_validator(cls, value):
#         """
#         Validate user birthday
#         """
#         if not value:
#             return ValueError("Укажите дату рождения")

#         age = relativedelta(datetime.now(), value.date()).years

#         if age > 99:
#             return ValueError("Укажите возраст поменьше")

#         if age < 18:
#             return ValueError("Возраст должен быть больше 18 лет")

#         cls.age = age
#         return value

#     @field_validator("firstname", "lastname", "middlename")
#     @classmethod
#     def fullname_validator(cls, value: str):
#         """
#         Validate user fullname first letter
#         """

#         if not value[:1].isupper():
#             return value[:1].upper() + value[1:]

#         return value
