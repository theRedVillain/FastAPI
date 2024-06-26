from fastapi import FastAPI , Response , status , HTTPException , Depends
from typing import Optional 
from pydantic import BaseModel
import psycopg2  
from .database import *
from .models import *
from . import models , schemas
from sqlalchemy.orm import Session
app = FastAPI() 

models.Base.metadata.create_all(bind=engine)
get_db()


while True:
    try:
        conn = psycopg2.connect(host="localhost",user="postgres",password="sonu",database="FastAPI")
        cursor = conn.cursor()  
        print("Connection Successfull") 
        break
    except Exception as e:
        print("Connection Failed") 
        print("Error Occured : ",e) 

## Get all posts 

@app.get("/all_posts")
def get_all_posts():
    try:
        cursor.execute("""SELECT * from  products""") 
        posts = cursor.fetchall() 
        print(1)
        return {'data' : posts} , status.HTTP_200_OK
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=e) 
    
@app.get("/single_post/{id}")
def get_single_post(id :int):
    try:
        cursor.execute("""SELECT * from products where pid = %s""" , (int(id) ,))
        post = cursor.fetchone() 
        return {'data':post} , status.HTTP_200_OK 
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=e) 
    
@app.post("/make_a_post")
def make_a_post_func(data : schemas.Posts):
    try:
        cursor.execute("""INSERT INTO products (name , price , inventory) VALUES (%s,%s,%s) RETURNING *""",(data.name , data.price , data.inventory))
        conn.commit()
        post = cursor.fetchone() 
        return {post} , status.HTTP_200_OK
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=e) 
    
@app.put("/update_post/{id}")
def update_post(id :int ,data : schemas.Posts):
    try:
        cursor.execute("""UPDATE products set price = %s where pid = %s returning *""",(data.price , id)) 
        conn.commit() 
        result = cursor.fetchone() 
        return {result} , status.HTTP_200_OK 
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=e) 
    
@app.delete("/delete_post/{id}")
def delete_func(id : int , response : Response):
    try:
        cursor.execute("""DELETE from products where pid = %s returning *""" , (id,))
        deleted_post = cursor.fetchone() 
        print(deleted_post) 
        return status.HTTP_204_NO_CONTENT  
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=e)
    
@app.get("/user/get_all_data")
def testing(db: Session = Depends(get_db)):
    data = db.query(models.User).all() 
    return data

@app.post("/user/user_entry")
def user_entry_function(user_entry : schemas.Users_Model , db: Session = Depends(get_db)):
    new_user = models.User(**user_entry.dict())
    db.add(new_user) 
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user/get_one_user/{id}")
def get_one_post(id : int , db: Session = Depends(get_db)):
    data = db.query(models.User).filter(models.User.user_id == id).first()
    return data

@app.delete("/user/delete_user/{id}")
def delete_user(id : int , db: Session = Depends(get_db)):
    deleted_post = db.query(models.User).delete(models.User.user_id == id)
    deleted_post.delete(synchronize_sessions=True)
    db.commit() 

@app.put("/user/update_user/{id}" , response_model=schemas.Return_Users)
def update_post(id: int ,user_entry : schemas.Users_Model, db: Session = Depends(get_db)):
    post = db.query(models.User).filter(models.User.user_id == id)

    if post.first() == None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = "User not found") 
    post.update(user_entry.dict()) 
    db.commit() 
    return post.first()










