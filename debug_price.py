from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_price_with_auth():
    # Register a new user
    register_response = client.post(
        "/api/v1/register/",
        data={
            "username": "debuguser3",
            "password": "debugpassword"
        }
    )
    
    print(f"Register status: {register_response.status_code}")
    print(f"Register response: {register_response.json()}")
    
    if register_response.status_code == 200:
        tokens = register_response.json()
        access_token = tokens['access_token']
        
        # Test creating price record with authentication
        price_data = {
            "work_type_children_id": 3,
            "price": 2500.0
        }
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Test creating price record
        price_response = client.post(
            '/api/v1/price/', 
            json=price_data,
            headers=headers
        )
        
        print(f"Price create status: {price_response.status_code}")
        try:
            print(f"Price create response: {price_response.json()}")
        except:
            print(f"Price create response text: {price_response.text}")
        
        # Test getting price record
        get_response = client.get(
            '/api/v1/price/3',
            headers=headers
        )
        
        print(f"Price get status: {get_response.status_code}")
        try:
            print(f"Price get response: {get_response.json()}")
        except:
            print(f"Price get response text: {get_response.text}")

if __name__ == "__main__":
    test_price_with_auth()