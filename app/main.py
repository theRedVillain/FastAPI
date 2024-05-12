from fastapi import FastAPI , Response , HTTPException ,status , Depends
from typing import Optional , Union
from pydantic import BaseModel 
from random import randrange
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models 
from .database import engine , get_db

models.Base.metadata.create_all(bind=engine)
get_db()


class DataModel(BaseModel):
    title : str 
    Price : int

class database_entry(BaseModel):
    name : str 
    quantity : int 
    on_sale : Optional[bool] 
    price : int 

class update_data(BaseModel):
    column : str 
    value : Optional[Union[str, int]]

class cinema_entry(BaseModel):
    movie_name : str 
    seats : int 

class update_cinema(BaseModel):
    movie_name : Optional[str] 
    seats : Optional[int]

app = FastAPI()

# Database Connection 
try:

    while True:

        conn = psycopg2.connect(host="localhost",user="postgres",password="1@12@23@34@4" , database="postgres" , cursor_factory=RealDictCursor)

        cursor = conn.cursor()

        print("Connection Successsfull")
        break
except Exception as e:
    print(e)
@app.get("/posts")
def get_all_posts():
        cursor.execute("""
                    SELECT * from products 
                    """)
        
        result = cursor.fetchall()
        print(result)
        return {"Data" : result} 

@app.post("/posts")
def make_a_post(data : database_entry , response : Response):
    try:
        data = data.dict() 
        print(data)
        result = cursor.execute("""INSERT INTO products (name , quantity , on_sale , price) VALUES(%s,%s,%s,%s) returning *""",(data['name'] , data['quantity'] , data['on_sale'] , data['price']))
        result = cursor.fetchone()
        conn.commit()
        response.status_code = status.HTTP_201_CREATED 
        print(result)
        return {"Data":result} 
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail= "Post not created")

@app.get("/posts/{id}")
def get_particular_posts(id : int):
    try:
        cursor.execute("""SELECT * from products where product_id = %s""" , (id , )) 
        data = cursor.fetchone() 
        return {"Data" : data} 
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail = str(e))

@app.put("/posts/{id}")
def update_posts(id : int , data : update_data):
    try:
        data = data.dict()
        result = cursor.execute(f"""UPDATE products SET {data['column']} = %s WHERE product_id = %s RETURNING *""" , (data['value'] , id))
        result = cursor.fetchone()
        conn.commit()
        print("Data Updated Successfully") 
        return {"Data" : result}
    
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=str(e))
    

@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    try:
        cursor.execute("""DELETE FROM products where product_id = %s returning *""" , (id ,))
        result = cursor.fetchone()
        conn.commit()
        print("Data Deleted Successfully")
        return {"Data" : result}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=str(e)) 
    
@app.get("/cinema/all_post")
def get_all_post(db: Session = Depends(get_db)):
    result = db.query(models.cinema_db).all()
    return {"Data" : result} 

@app.post("/cinema/make_post") 
def make_a_post( data : cinema_entry  , db: Session = Depends(get_db)):
    try:
        new_post = models.cinema_db(**data.dict())
        db.add(new_post)
        db.commit() 
        db.refresh(new_post)
        return {"Data" : new_post} 
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Post not created")
        
@app.get("/cinema/only_one/{id}")
def get_only_one_post(id : int , db: Session = Depends(get_db)):
    try:
        post = db.query(models.cinema_db).filter(models.cinema_db.id == id)
        if post.first() == None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = f'Entry with id {id} not present in database') 
        return {"Data" : post.first()} 
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail = str(e)) 

@app.delete("/cinema/delete_post/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_content(id : int ,db: Session = Depends(get_db)):
    try:
        post = db.query(models.cinema_db).filter(models.cinema_db.id == id)
        if post.first() == None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = f'Entry with id {id} not present in database')  
        post.delete(synchronize_session=False) 
        db.commit()
        return {"Message":"Post Deleted Successfully"} 
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail = str(e)) 
    
@app.put("/cinema/update__content/{id}")
def update_content_func(id : int , data : update_cinema, db: Session = Depends(get_db)):
    try:
        post = db.query(models.cinema_db).filter(models.cinema_db.id == id)
        if post.first() == None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = f'Entry with id {id} not present in database') 
        post.update(data.dict() , synchronize_session=False)
        db.commit() 
        return {"Data" : post.first()} 
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Update failed")
