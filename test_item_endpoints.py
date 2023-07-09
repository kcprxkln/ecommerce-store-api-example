import requests
from api import Item
from pymongo import MongoClient 

### SPLIT TESTS FROM ITEM AND CUSTOMER FOR TWO INDEPENDENT FILES ###

API_URL = 'http://127.0.0.1:8000'

client = MongoClient("mongodb://localhost:27017")

DB_NAME = "store_db"

db = client[DB_NAME]

items_db = db['items']


item_obj_highest_id = items_db.find_one(sort=[("serial_id", -1)]) #returns object with the highest id

if item_obj_highest_id:
    item_highest_id = item_obj_highest_id['serial_id']

else:
    print('There are no documents in the \"items" collection')
    item_highest_id = 1 


test_item = Item(
    serial_id=item_highest_id + 1000, 
    name='White T-Shirt',
    price=24.99,
    stock=3200,
    added='12-08-2020'
)

test_item_2 = Item(
    serial_id=item_highest_id + 2000, 
    name='White T-Shirt',
    price=24.99,
    stock=3200,
    added='12-08-2020'
)

test_item_serial_id = str(test_item.dict()["serial_id"])


item_endpoints = {
    "add": API_URL + '/items/add',
    "search": API_URL + '/items/search',
    "delete": API_URL + '/items/delete/' + test_item_serial_id,
    "update": API_URL + '/items/update/' + test_item_serial_id
}


def test_add_new_item(item: Item = test_item, endpoint: str = item_endpoints['add']) -> None:
    response = requests.post(
        url=endpoint, 
        json=item.dict(),
        headers={'Content-Type':'application/json'}
        )
    
    assert response.status_code == 200


def test_search_item(endpoint: str = item_endpoints['search']) -> None:
    params = test_item.dict()
    response = requests.get(
        url=endpoint, 
        params=params
    )

    assert response.status_code == 200


def test_update_item(updated_item: Item = test_item_2, endpoint: str = item_endpoints['update']) -> None:
    response = requests.put(
        url=endpoint, 
        json=updated_item.dict(), 
        headers={'Content-Type': 'application/json'}        
    )

    assert response.status_code == 200


def test_check_if_id_exists(item: Item = test_item, second_item: Item = test_item_2) -> None:
    
    #Create second item with another serial_id
    requests.post(
        url=item_endpoints['add'], 
        json=item.dict(),
        headers={'Content-Type':'application/json'}
        )
    
    #Attempt to assign serial number of item to the second item that should raise 409 error
    response = requests.put(
        url=item_endpoints['update'],
        json=second_item.dict(),
        headers={'Content-Type': 'application/json'} 
    )

    assert response.status_code == 409
    

def test_delete_item(endpoint: str = item_endpoints['delete']) -> None:
    response = requests.delete(url=endpoint)
    response.raise_for_status()

    assert response.status_code == 200
    
    ## Deleting second object that was created during the tests
    requests.delete(url=API_URL + '/items/delete/' + str(test_item_2.dict()['serial_id']))
