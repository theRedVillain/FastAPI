from .database import Base 
from sqlalchemy import Column , Integer , String , Boolean , DateTime , literal_column
from sqlalchemy.sql import func


class cinema_db(Base):
    __tablename__ = "cinema" 

    id = Column(Integer , primary_key=True , nullable= False) 
    movie_name = Column(String , unique=True , nullable=False) 
    seats = Column(Integer , nullable=False , server_default='1000')
    time_of_entry = Column(DateTime(timezone=True), server_default=func.now()) 


