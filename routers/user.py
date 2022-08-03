from bson import ObjectId
from fastapi import Depends, HTTPException,APIRouter
from typing import List
from sqlalchemy import true
from db.mongodb import get_database
from model import User, UserOut
from motor.motor_asyncio import AsyncIOMotorClient
from helper import PyObjectId



database_name = "fastapicluster"
collection_user_name = "users"

router = APIRouter()

@router.post("/", tags=["users"])
async def user_create(
    payload : User,
    db : AsyncIOMotorClient = Depends(get_database)
):
    
    new_user = payload.dict()
    db_user = await db[database_name][collection_user_name].insert_one(new_user)
    return true

@router.get('/', tags=["users"])
async def get_all_user(
    db : AsyncIOMotorClient = Depends(get_database)
):
    users : List[UserOut] = [] 
    db_users =  db[database_name][collection_user_name].find({})
    
    async for user in db_users:
        users.append(UserOut(id = user["_id"] , name = user["name"] , phone=user["phone"], age= user["age"]))
        
    return users
    
@router.get('/{user_id}', tags=["users"])
async def get_user_by_id(
        user_id:str,
        db : AsyncIOMotorClient = Depends(get_database)
):
    db_user = await db[database_name][collection_user_name].find_one({"_id" : ObjectId(user_id)})
    
    
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return UserOut(**db_user)

@router.patch("/{user_id}", tags=["users"])
async def update_user(
    user_update:dict ,
    user_id:str,
    db : AsyncIOMotorClient = Depends(get_database)
    ):
    db_user = await db[database_name][collection_user_name].find_one({"_id" : ObjectId(user_id)})   
    
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
       
    myquery = { "_id": ObjectId(user_id) }
    newvalues = { "$set": user_update}

    updated_user = db[database_name][collection_user_name].update_one(myquery, newvalues)
    
    return True

@router.delete("/{user_id}", tags=["users"])
async def user_delete(
    user_id :str,
    db : AsyncIOMotorClient = Depends(get_database)
):
    db_user = await db[database_name][collection_user_name].find_one({"_id" : ObjectId(user_id)})
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    deleted = await db[database_name][collection_user_name].delete_one({"_id" : ObjectId(user_id)})
    
    return True if deleted.deleted_count == 1 else False

