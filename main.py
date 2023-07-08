from fastapi import FastAPI, HTTPException, status
from pymongo import MongoClient 
from models import Item, Customer


client = MongoClient("mongodb://localhost:27017")

DB_NAME = "store_db"

db = client[DB_NAME]

items_db = db['items']
customers_db = db['customers']


app = FastAPI(
    title="FastAPI + mongoDB ecommerce store",
    description="An example of API for ecommerce store created with FastAPI and mongoDB"
)


@app.post('/items/add', tags=["Items"])
def add_new_item(item: Item):
    items_db.insert_one(item.dict())
    return {"item added with id": item.serial_id}


@app.get('/items/search', tags=["Items"])
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


@app.put('/items/update/{serial_id}', tags=["Items"])
def update_item(serial_id: int, edited_item: Item):
    
    #Checking if the item with such ID already exists, since the ID needs to be Unique
    new_serial_id = edited_item.dict()['serial_id']
    
    def check_if_id_exists(id: int = new_serial_id) -> bool:
        current_id = items_db.find_one({"serial_id": id})
        return current_id

    if check_if_id_exists():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Item with that serial_id already exists.")
    
    else:
        update = {"$set": edited_item.dict()}
        items_db.update_one({"serial_id": serial_id}, update)
        return {f"updated": {serial_id}}    


@app.delete('/items/delete/{serial_id}', tags=["Items"])
def delete_item(serial_id: int):
    items_db.delete_one({"serial_id": serial_id})
    return {f"deleted": {serial_id}}
