from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional, List
from helper import PyObjectId


class UserUpdateRequest(BaseModel):
    name: str = ""
    username :Optional[str]
    phone : Optional[str]
    
class User(BaseModel):
    name : str
    username : str
    phone : Optional[str] = "111111111"
    
class UserOut(BaseModel):
    _id : PyObjectId = Field(default_factory=PyObjectId, alias="id")
    name : str
    phone : Optional[str] = "111111111"
    

class Book(BaseModel):
    author: PyObjectId = Field(default_factory=PyObjectId,alias="author_id")
    bookname: str
    email:str
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        
class BooksOut(BaseModel):
    _id : PyObjectId = Field(default_factory=PyObjectId, alias="id")
    author:Optional[PyObjectId] = Field(default_factory=PyObjectId,alias="author_id")
    bookname: str
    email: str
    
class BookUpdateRequest(BaseModel):
    author: Optional[PyObjectId] = Field(default_factory=PyObjectId,alias="author_id")
    bookname: str=""
    email:Optional[str]
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
    


    