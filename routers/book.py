from bson import ObjectId
from fastapi import Depends,HTTPException,APIRouter
from typing import List
from pydantic import PyObject
from sqlalchemy import true
from db.mongodb import get_database
from helper import PyObjectId
from model import BooksOut, BooksOutWithUser,Book
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

database_name = "fastapicluster"
collection_book_name ="books"

@router.post("/create", tags=["books"])
async def book_create(
    payload : Book,
    db : AsyncIOMotorClient = Depends(get_database)
):
    new_book = payload.dict()
    db_book = await db[database_name][collection_book_name].insert_one(new_book)
    return true

@router.get("/", tags=["books"])
async def get_all_books(
    db : AsyncIOMotorClient = Depends(get_database)
):
    books : List[BooksOut] = [] 
    db_book =  db[database_name][collection_book_name].find({})
    
    
    async for a in db_book:
        print(a["author"])
        books.append(BooksOut(id =a["_id"], author =a["author"] ,bookname= a["bookname"]  ))
        
    return books
 
@router.get("/get/{book_id}", tags=["books"])
async def get_book_by_id(
        book_id:str,
        db : AsyncIOMotorClient = Depends(get_database)
):
    bookwithuser : List[BooksOutWithUser] = []
    db_book = db[database_name][collection_book_name].aggregate( [

        
        {   
            "$match": {"_id" : ObjectId(book_id) }
        },
        {
            "$lookup":
                {
                "from": "users", #Nereden
                "localField": "author",#Bağlantı
                "foreignField": "_id",#Bağlantı
                "as": "user"#Yazdırlan Isim
                }
        },
        {
            "$unwind": "$user"
        }
    
    ])
    async for book in db_book:
        bookwithuser.append(BooksOutWithUser(**book))
        
    return bookwithuser

@router.patch("/update/{book_id}", tags=["books"])
async def update_book(
    book_update:dict,
    book_id:str,
    db : AsyncIOMotorClient = Depends(get_database)
    ):
    db_book = await db[database_name][collection_book_name].find_one({"_id" : ObjectId(book_id)})

    if not db_book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    
       
    myquery = { "_id": ObjectId(book_id) }
    newvalues = { "$set": book_update}

    updated_book = db[database_name][collection_book_name].update_one(myquery, newvalues)
    
    return True



@router.delete("/delete/{book_id}", tags=["books"])
async def book_delete(
    book_id :str,
    db : AsyncIOMotorClient = Depends(get_database)
):
    db_book = await db[database_name][collection_book_name].find_one({"_id" : ObjectId(book_id)})
    if not db_book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    
    deleted = await db[database_name][collection_book_name].delete_one({"_id" : ObjectId(book_id)})
    
    return True if deleted.deleted_count == 1 else False
