import requests
from main import Customer, Item
from pymongo import MongoClient 
import pytest

API_URL = 'http://127.0.0.1:8000'

client = MongoClient("mongodb://localhost:27017")

DB_NAME = "store_db"

db = client[DB_NAME]

items_db = db['items']
customers_db = db['customers']


item_obj_highest_id = items_db.find_one(sort=[("serial_id", -1)]) #returns object with the highest id

if item_obj_highest_id:
    item_highest_id = item_obj_highest_id['serial_id']

else:
    print('There are no documents in the \"items" database')
    item_highest_id = 1 

# customer_obj_highest_id = customers_db.find_one(sort=[("id", -1)]) 
# customer_highest_id = customer_obj_highest_id['id']

test_item = Item(
    serial_id=item_highest_id + 1000, 
    name='White T-Shirt',
    price=24.99,
    stock=3200,
    added='12-08-2020'
)


item_endpoints = {
    "add": API_URL + '/items/add',
    "search": API_URL + '/items/search',
    "delete": API_URL + '/items/delete/' + str(test_item.dict()["serial_id"]),
    "update": API_URL + '/items/update/' + str(test_item.dict()["serial_id"])
}


def test_add_new_item(item: Item = test_item, endpoint: str = item_endpoints['add']) -> None:
    response = requests.post(
        url=endpoint, 
        json=item.dict(),
        headers={'Content-Type':'application/json'})
    response.raise_for_status()
    
    assert response.status_code == 200


def test_search_item(endpoint: str = item_endpoints['search']) -> None:
    params = test_item.dict()
    response = requests.get(
        url=endpoint, 
        params=params
    )
    response.raise_for_status()

    assert response.status_code == 200


def test_delete_item(endpoint: str = item_endpoints['delete']) -> None:
    response = requests.delete(url=endpoint)
    response.raise_for_status()

    assert response.status_code == 200\
    

def test_update_item(item: Item = test_item, endpoint: str = item_endpoints['update']) -> None:
    response = requests.put(
        url=endpoint, 
        json=item.dict(), 
        headers={'Content-Type': 'application/json'}        
    )
    response.raise_for_status()

    assert response.status_code == 200