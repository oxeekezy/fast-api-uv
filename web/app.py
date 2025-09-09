from fastapi import FastAPI
from web.users.router import router


app = FastAPI()
app.include_router(router)


@app.get("/")
def read_root():
    """
    Hello world endpoint
    """
    return {"Hello": "World"}
