from fastapi import FastAPI , Response , HTTPException ,status
from typing import Optional , Union
from pydantic import BaseModel 
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

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


app = FastAPI()

data_collection = [{"title" : "The Haunted Ship" , "Price" : 260 , "id" : 24242},{"title" : "The Runner" , "Price" : 1260 ,"id" : 23232},{"title" : "Laapta Ladies" , "Price" : 660 , "id" : 1212}] 

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
        


