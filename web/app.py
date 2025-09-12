from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from web.admin.auth import AdminAuth
from web.admin.views import CourseAdminView, UsersAdminView
from web.users.router import router as user_router
from web.courses.router import router as course_router
from web.images.router import router as images_router
from random import randint
from time import sleep
from asyncio import sleep as asleep
from sqladmin import Admin
from web.database import ENGINE
from web.admin.auth import authentication_backend
from redis import asyncio as aioredis
from web.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(course_router)
app.include_router(images_router)

admin = Admin(app=app, engine=ENGINE, authentication_backend=authentication_backend)
admin.add_view(UsersAdminView)
admin.add_view(CourseAdminView)


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

