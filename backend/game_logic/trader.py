import requests

API_LINK = "http://localhost:8000"

class Trader():
    def __init__(self, balance):
        self.balance = balance

    def place_order(self, ticker, quantity, order_type):

        order_url = API_LINK + "/orders"

        payload = {
            "ticker": ticker,
            "quantity": quantity,
            "type": order_type
        }

        response = requests.post(order_url, params=payload)
        
        return response.json()