from fastapi import FastAPI , Response , HTTPException ,status
from typing import Optional 
from pydantic import BaseModel 
from random import randrange

class DataModel(BaseModel):
    title : str 
    Price : int

app = FastAPI()

data_collection = [{"title" : "The Haunted Ship" , "Price" : 260 , "id" : 24242},{"title" : "The Runner" , "Price" : 1260 ,"id" : 23232},{"title" : "Laapta Ladies" , "Price" : 660 , "id" : 1212}] 

@app.get("/posts")
def get_all_posts():
    return {"Data" : data_collection} 

@app.post("/posts")
def make_a_post(data : DataModel , response : Response):
    try:
        id = randrange(1,100000000)
        data = data.dict() 
        data['id'] = id 
        data_collection.append(data) 
        response.status_code = status.HTTP_201_CREATED 
        return {"Data":data_collection} 
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail= "Post not created")

@app.get("/posts/{id}")
def get_particular_posts(id : int):
    for i in data_collection:
        if i['id'] == id : 
            return i 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail= "NO such post") 

@app.put("/posts/{id}")
def update_posts(id : int , data : DataModel):
    data = data.dict()
    for i in data_collection:
        if i['id'] == id:
            i['title'] = data['title']
            i['Price'] = data['Price'] 
            return {"New Data" : get_particular_posts(id)} 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , details = "NO such Post exists")

@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    for i in data_collection:
        if i['id'] == id:
            data_collection.remove(i) 
            return {"Response":status.HTTP_204_NO_CONTENT} 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , details= "No such Post")
        


