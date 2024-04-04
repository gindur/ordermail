import base64
import os
import requests
import data.keys as keys
import json
from json import JSONEncoder
from collections import namedtuple
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

qb_api_key = os.getenv("QB_API_KEY")

#Endpoint
ORDER_ENDPOINT = keys.orders_endpoint
#Auth
ENCODED_AUTH = keys.encoded_auth
#Header
header = {
        "Authorization": f"Basic {ENCODED_AUTH}"
    }

class RawOrder:
    def __init__(self, order_id, date_created, total_amount, status):
        self.order_id = order_id
        self.date_created = date_created
        self.total_amount = total_amount
        self.status = status

    def print_attributes(self):
        for attr, value in self.__dict__.items():
            print(f"{attr}: {value}")

class Order:
    def __init__(self, order_id, date_created, total_amount, status):
        self.order_id = order_id
        self.date_created = date_created
        self.total_amount = total_amount
        self.status = status

    def print_attributes(self):
        for attr, value in self.__dict__.items():
            print(f"{attr}: {value}")

def fetch_order_data():

    response = requests.get(ORDER_ENDPOINT, headers=header)

    if response.status_code == 200:
        # Process and return the customer data
        return [RawOrder(order['order_id'], order['date_created'], order['total_amount'], order['status']) for order in response.json()]
 
    else:
        #Error handling
        return {"error": "Failed to fetch order data", "status_code": response.status_code, "response": response.text}

# [RawOrder] -> [Order]
def fetch_detailed_order_data(data):
    orders = []
    for order in data:
        url = ORDER_ENDPOINT + "/{}".format(order.order_id)
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            orders.append(response.json())
            continue
        else:
            print({
                "error": "Failed to fetch specific order data for order: {}".format(order.order_id),
                "status_code": response.status_code,
                "response": response.text
            })
    return orders

def fetch_order(order_id):
    url = ORDER_ENDPOINT + f'?order_id={order_id}'
    print(url)
    response = requests.get(url,headers=header)
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch order data", "status_code": response.status_code, "response": response.text}



if __name__ == "__main__":
    
    data = fetch_order_data()
    orders = fetch_detailed_order_data(data)
    print(data)
