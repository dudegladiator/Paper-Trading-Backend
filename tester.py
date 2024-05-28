import http.client
import json

def test_authenticate(base_url: str, api_key: str):
    conn = http.client.HTTPConnection(base_url)
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Send the POST request to the /authenticate endpoint with api_key as a query parameter
    conn.request("POST", f"/authenticate?api_key={api_key}", headers=headers)
    
    response = conn.getresponse()
    data = response.read().decode()
    
    # Parse the response data
    result = json.loads(data)
    
    print(f"Status: {response.status}")
    print(f"Response: {result}")
    
    conn.close()
    
def test_get_user_data(base_url: str, api_key: str, token: str):
    conn = http.client.HTTPConnection(base_url)
    
    headers = {
        'Content-Type': 'application/json',
        'api-key': api_key,
        'token': token
    }
    
    # Send the GET request to the /user endpoint
    conn.request("GET", "/user", headers=headers)
    
    response = conn.getresponse()
    data = response.read().decode()
    
    # Parse the response data
    result = json.loads(data)
    
    print(f"Status: {response.status}")
    print(f"Response: {result}")
    
    conn.close()

from datetime import datetime
import json

def test_execute_trade(base_url: str, api_key: str, token: str, trade_data: dict):
    conn = http.client.HTTPConnection(base_url)
    
    headers = {
        'Content-Type': 'application/json',
        'api-key': api_key,
        'token': token
    }
    
    # Create the payload for the request
    payload = json.dumps(trade_data)
    
    # Send the POST request to the /trade endpoint
    conn.request("POST", "/trade", body=payload, headers=headers)
    
    response = conn.getresponse()
    data = response.read().decode()
    
    # Parse the response data
    result = json.loads(data)
    
    print(f"Status: {response.status}")
    print(f"Response: {result}")
    
    conn.close()
    
    
import httpx
BASE_URL = "http://localhost:8992/api"

def test_get_portfolio():
    response = httpx.get(f"{BASE_URL}/portfolio", headers={"api-key": "49127765"})
    print("Portfolio:", response.json())

def test_get_transaction():
    response = httpx.get(f"{BASE_URL}/transaction", headers={"api-key": "49127765"})
    print("Transaction:", response.json())

def test_fetch_user():
    response = httpx.get(f"{BASE_URL}/user", headers={"api-key": "49127765"})
    print("User:", response.json())

def test_get_dashboard():
    response = httpx.get(f"{BASE_URL}/dashboard", params={"team": "tester"})
    print("Dashboard:", response.json())


if __name__ == "__main__":
    test_get_portfolio()
    test_get_transaction()
    test_fetch_user()
    test_get_dashboard()
    
    base_url = "localhost:4546"
    test_api_key = "45harsh45"
    # reply = test_authenticate(base_url, test_api_key)
    test_token = "4786162514536978562"  # Replace with a valid token
    # test_get_user_data(base_url, test_api_key, test_token)
    trade_data = {
        "action": "sell",  # or "sell"
        "stockName": "AAPL",
        "stockPrice": 150.0,
        "quantity": 5,
        "balance": 1500.0,
        "date": datetime.now().isoformat()  # Use the correct date format
    }
    # test_execute_trade(base_url, test_api_key, test_token, trade_data)

