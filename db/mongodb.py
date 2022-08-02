from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    client : AsyncIOMotorClient = None
    
db_obj = Database()
    
async def get_database() -> AsyncIOMotorClient:
    return db_obj.client


async def connect_to_mongo() -> AsyncIOMotorClient:
    db_obj.client = AsyncIOMotorClient("mongodb+srv://izgin:f7eD471JMI6KDcDG@fastapicluster.v8bunoo.mongodb.net/?retryWrites=true&w=majority")
    