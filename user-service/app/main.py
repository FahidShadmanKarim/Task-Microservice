from fastapi import FastAPI
from app.api.v1.endpoint import users,auth
from app.core.config import Base,engine
from fastapi_pagination import add_pagination

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(users.router,prefix="/api",tags=["Users"])
app.include_router(auth.router, prefix="/api", tags=["Auth"])

add_pagination(app)


@app.get('/')
def read_root():
    return {"message": "Hello, World!"}