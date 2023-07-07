from fastapi import FastAPI
from pymongo import MongoClient 
from pydantic import BaseModel
from datetime import datetime


client = MongoClient("mongodb://localhost:27017")

DB_NAME = "store_db"

db = client[DB_NAME]

items_db = db['items']
customers_db = db['customers']

class Customer(BaseModel):
    id: int
    first_name: str
    last_name: str 
    email: str
    is_verified: bool

class Item(BaseModel):
    serial_id: int
    name: str
    price: float
    stock: int
    added: str


app = FastAPI(
    title="FastAPI + mongoDB ecommerce store",
    description="example of API for ecommerce shop created with FastAPI and mongoDB"
)


@app.post('/items/add')
def add_new_item(item: Item):
    items_db.insert_one(item.dict())
    return {"item added with id": item.serial_id}


@app.get('/items/search')
def query_by_params(
    serial_id: int or None = None,
    name: str or None = None, 
    price: float or None = None, 
    stock: int or None = None, 
    added: str or None = None
):
    def check_if_matches():
        query = {}

        if serial_id is not None:
            query['serial_id'] = serial_id
        if name is not None:
            query['name'] = name
        if price is not None:
            query['price'] = price
        if stock is not None:
            query['stock'] = stock
        if added is not None:
            query['added'] = added

        results = items_db.find(query)
        items = [Item(**item) for item in results]
        return items

    return check_if_matches()


@app.delete('/items/delete/{serial_id}')
def delete_item(serial_id: int):
    items_db.delete_one({"serial_id": serial_id})
    return {f"deleted": {serial_id}}


@app.put('/items/update/{item_id}')
def update_item(item_id: int):
    return {f"updated": {item_id}}


