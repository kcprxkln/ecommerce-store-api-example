import requests
from main import Customer, Item
from pymongo import MongoClient 


API_URL = 'http://127.0.0.1:8000'

client = MongoClient("mongodb://localhost:27017")

DB_NAME = "store_db"

db = client[DB_NAME]

items_db = db['items']
customers_db = db['customers']


item_obj_highest_id = items_db.find_one(sort=[("serial_id", -1)]) #returns object with the highest id
item_highest_id = item_obj_highest_id['serial_id']                #fetches the serial id from that object

# customer_obj_highest_id = customers_db.find_one(sort=[("id", -1)]) 
# customer_highest_id = customer_obj_highest_id['id']

endpoints = {
    "add_item" : API_URL + '/items/add',
    "search_item" : API_URL + '/items/search'
}

test_item = Item(
    serial_id=item_highest_id + 1000, 
    name='White T-Shirt',
    price=24.99,
    stock=3200,
    added='12-08-2020'
)

def test_add_new(item: Item = test_item, endpoint: str = endpoints['add_item']) -> None:
    response = requests.post(
        url=endpoint, 
        json=item.dict(),
        headers={'Content-Type':'application/json'})
    response.raise_for_status()
    
    assert response.status_code == 200


def test_search(endpoint: str = endpoints['search_item']) -> None:
    params = test_item.dict()
    response = requests.get(
        url=endpoint, 
        params=params
    )
    response.raise_for_status()

    assert response.status_code == 200