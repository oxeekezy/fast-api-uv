from fastapi import Depends, FastAPI
from web.admin.views import UsersAdminView
from web.auth.scheme import get_bearer_token
from web.users.router import router
from random import randint
from time import sleep
from asyncio import sleep as asleep
from sqladmin import Admin
from web.database import ENGINE


app = FastAPI()
app.include_router(router)

admin = Admin(app=app, engine=ENGINE)
admin.add_view(UsersAdminView)


@app.get("/")
def read_root():
    """
    Hello world endpoint
    """
    return {"Hello": "World"}

@app.get("/test_sync/{id}")
def test_sync(id: int):
    time_to_wait = randint(3,10)
    sleep(time_to_wait)
    return {"msg": f"Задача с id: {id} завершена. Время выполнения: {time_to_wait}с."}

@app.get("/test_async/{id}")
async def test_async(id: int):
    time_to_wait = randint(3,10)
    asleep(time_to_wait)
    return {"msg": f"Задача с id: {id} завершена. Время выполнения: {time_to_wait}с."}
