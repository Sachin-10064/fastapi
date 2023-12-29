from fastapi import FastAPI
# from .blog import models
# from .blog.database import engine
from typing import Union
from pydantic import BaseModel
app = FastAPI()

# models.Base.metadata.create_all(engine)

@app.get("/")
async def blog():
    return {"message": "Hello World"}

@app.get("/blog/{id}/comments")
def blogComment():
    return {'data': {"comments": {"good", "Very Good", "excellent"}}}

@app.get("/blog/{id}")
async def BlogById(id: int):
    # return {"message": f"Hello {id}"}
    return {"data": id}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.get("/items/")
async def read_item(skip: int=0 , limit: int = 10):
    return {"message": f"skip {skip} limit {limit}"}
    # return fake_items_db[skip : skip + limit]

@app.post("/items/")
async def create_item(item: Item):
    return item

