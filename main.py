import time
from fastapi import Depends, FastAPI ,APIRouter, Request
from typing import List
from sqlalchemy import true
from db.mongodb import connect_to_mongo
from motor.motor_asyncio import AsyncIOMotorClient
# from dependencies.dependencies import get_token_header,get_query_token
from routers import user , book


app = FastAPI()#dependencies=[Depends(get_query_token)])

app_router = APIRouter()
app.add_event_handler('startup' , connect_to_mongo)

app.include_router(
    user.router,
    prefix="/user",
  #  dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
app.include_router(book.router , prefix="/book")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(process_time)
    return response



