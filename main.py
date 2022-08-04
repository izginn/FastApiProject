import time
from fastapi import FastAPI ,APIRouter, Request
from db.mongodb import connect_to_mongo
from routers import user, book
from starlette.middleware.cors import CORSMiddleware
import main
# from dependencies.dependencies import get_token_header,get_query_token

app = FastAPI()#dependencies=[Depends(get_query_token)])

app_router = APIRouter()
app.add_event_handler('startup' , connect_to_mongo)

app.include_router(
    user.router,
    prefix="/users",
 
)
app.include_router(book.router , prefix="/books")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
