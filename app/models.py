from sqlalchemy.orm import relationship
from sqlalchemy import Column , String , Integer , Boolean , TIMESTAMP , func
from .database import Base 


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer , primary_key= True  , autoincrement=True) 
    name = Column(String , nullable=False) 
    prime_member = Column(Boolean , nullable=False , server_default="False")
    order_time = Column(TIMESTAMP, nullable=False , server_default=func.now())

class User_Onboarding(Base):
    __tablename__ = 'onboarding_users' 
    id = Column(Integer , primary_key=True , autoincrement=True)
    email = Column(String , nullable=False , unique=True) 
    password = Column(String , nullable=False)
    