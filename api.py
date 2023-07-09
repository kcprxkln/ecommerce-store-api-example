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


## ITEMS ENDPOINTS

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


## CUSTOMERS ENDPOINTS

@app.post('/customers/add', tags=['Customers'])
def add_customer(customer: Customer):
    #check if email is really email (if contains exactly 1 x @ and @ place isn't [0] or [-1], in the string must be at least one ".")
    #if it's not, raise an error
    def check_if_str_is_email(email: str = str(customer.dict()['email'])) -> bool:
        
        def count_occurrences(email: str = email, count_chars: list[str] = ['@', '.']):
            occurrences = {char: email.count(char) for char in count_chars}
            return occurrences 

        if count_occurrences()['@'] == 1 and count_occurrences()['.'] >= 1:
            
            if email[0] == "@" or email[-1] == "@":
                return False
            else:
                return True
            
        else: 
            return False

    if check_if_str_is_email():
        customers_db.insert_one(customer.dict())
        return {"Added customer with id": customer.id}
    
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid email format')


@app.get('/customers/search', tags=['Customers'])
def search_customer(
    id: int or None = None, 
    first_name: str or None = None, 
    last_name: str or None = None, 
    email: str or None = None,
    is_verified: bool or None = None
):
    def check_if_matches():
        query = {}

        if id is not None:
            query['id'] = id
        if first_name is not None:
            query['first_name'] = first_name
        if last_name is not None:
            query['last_name'] = last_name
        if email is not None:
            query['email'] = email
        if is_verified is not None:
            query['is_verified'] = is_verified

        results = customers_db.find(query)
        customers = [Customer(**customer) for customer in results]
        return customers

    return check_if_matches()

@app.put('/customers/update/{id}', tags=['Customers'])
def update_customer(id: int, edited_customer: Customer):

#Checking if the Customer with such ID already exists, since the ID needs to be Unique    
    new_customer_id = edited_customer.dict()['id']
    
    def check_if_id_exists(id: int = new_customer_id) -> bool:
        current_id = customers_db.find_one({"id": id})
        return current_id

    if check_if_id_exists():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Customer with that ID already exists.")
    
    else:
        update = {"$set": edited_customer.dict()}
        items_db.update_one({"serial_id": id}, update)
        return {f"updated": {id}}    


@app.delete('/customers/delete/{id}', tags=['customers'])
def delete_customer(id: int):
    customers_db.delete_one({"serial_id": id})
    return {f"deleted": {id}}