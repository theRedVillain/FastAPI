from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Posts(BaseModel):
    name : str 
    inventory : Optional[int] = 0 
    price : int

class Users_Model(BaseModel):
    name : str 
    prime_member : Optional[bool] = False

class Return_Users(BaseModel):
    name : str
    order_time : datetime
    class Config:
        orm_mode = True 
    