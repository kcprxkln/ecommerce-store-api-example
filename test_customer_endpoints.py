import requests
from api import Customer
from pymongo import MongoClient 


API_URL = 'http://127.0.0.1:8000'

client = MongoClient("mongodb://localhost:27017")

DB_NAME = "store_db"

db = client[DB_NAME]

items_db = db['customers']



customer_obj_highest_id = items_db.find_one(sort=[("id", -1)]) #returns object with the highest id

if customer_obj_highest_id:
    customer_highest_id = customer_obj_highest_id['id']

else:
    print('There are no documents in the \"customers" collection')
    customer_highest_id = 1 


test_customer = Customer(
    id=customer_highest_id,
    first_name="John", 
    last_name="Doe",
    email="john.doe@email.com",
    is_verified=True
)

test_customer_2 = Customer(
    id=customer_highest_id + 100,
    first_name="John", 
    last_name="Doe",
    email="john.@email.com",
    is_verified=True
)

test_customer_id = str(test_customer.dict()['id'])
test_customer_2_id = str(test_customer_2.dict()['id'])

endpoints = {
    'add': API_URL + '/customers/add', 
    'search': API_URL + '/customers/search/',
    'update': API_URL + '/customers/update/' + test_customer_id,
}


def test_add_new_customer(customer: Customer = test_customer, endpoint: str = endpoints['add']) -> None:
    response = requests.post(
        url=endpoint,
        json=customer.dict(),
        headers={'Content-Type':'application/json'}
    )
    
    assert response.status_code == 200


def test_add_customer_invalid_email(customer: Customer = test_customer, endpoint: str = endpoints['add']) -> None:
    all_passed = True
    invalid_mail_customer = customer.dict()
    corner_cases = ['thisisnotemail', '@notmail', '@notmail.com', 'not@mail','@not.mail@']

    for email_address in corner_cases:
        invalid_mail_customer['email'] = email_address
        invalid_mail_customer['id'] += 100
        response = requests.post(
            url=endpoint, 
            json=invalid_mail_customer,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code != 200:
            all_passed = False

    assert all_passed


def test_search_customer(customer: Customer = test_customer, endpoint: str = endpoints['search']) -> None:
    params = customer.dict()
    response = requests.get(
        url=endpoint, 
        params=params
    )

    assert response.status_code == 200


def test_update_customer(new_customer_data: Customer = test_customer_2, endpoint: str = endpoints['update']) -> None:

    response = requests.put(
        url=endpoint,
        json=new_customer_data.dict(),
        headers={'Content-Type':'application/json'}
    )

    assert response.status_code == 200


def test_update_customer_existing_id(customer: Customer = test_customer_2) -> None:

    requests.post(
        url=endpoints['add'],
        json=customer.dict(),
        headers={"Content-Type": "application/json"}
    )

# test if it is possible to change the initial customer ID to the edited one
    response = requests.put(
        url=endpoints['update'], 
        json=customer.dict(),
        headers={'Content-Type':'application/json'}                     
    )

    assert response.status_code == 409

