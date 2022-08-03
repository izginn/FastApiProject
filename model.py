from dataclasses import field
from datetime import datetime
from bson import ObjectId
from numpy import byte
from pydantic import BaseModel, Field
from typing import Optional, List
from helper import PyObjectId


class UserUpdateRequest(BaseModel):
    _id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    name: str = ""
    username :Optional[str]
    phone : Optional[str]
    email: Optional[str]
    age:Optional[bytes]
class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name : str
    username : str
    phone : Optional[str] = "111111111"
    email: Optional[str]
    age:Optional[bytes]
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class UserOut(BaseModel):
    id : PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name : str
    phone : Optional[str] = "111111111"
    email: Optional[str]
    age:Optional[bytes]
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class Book(BaseModel):
    author: PyObjectId = Field(default_factory=PyObjectId,alias="author")
    bookname: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        
class BooksOut(BaseModel):
    id : PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    author: PyObjectId
    bookname: str
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
    
class BookUpdateRequest(BaseModel):
    author: Optional[PyObjectId] = Field(default_factory=PyObjectId,alias="author_id")
    bookname: str=""
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class BooksOutWithUser(BaseModel):
    _id : PyObjectId = Field(default_factory=PyObjectId, alias="id")
    bookname: str
    email: str
    user: UserOut
 
