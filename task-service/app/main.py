from fastapi import FastAPI
from app.core.config import Base, engine
from app.api.v1.endpoint import task
from fastapi_pagination import add_pagination
from app.models.board_model import Board
from app.models.task_model import Task
from app.models.board_members import BoardMembers


app = FastAPI()

@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

app.include_router(task.router, prefix="/api", tags=["Tasks"])

add_pagination(app)

@app.get('/')
def read_root():
    return {"Message": "Hello Task!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)