import requests
import json

# First, register a user to get a token
register_data = {
    'username': 'testuser3',
    'password': 'testpassword'
}

try:
    # Register user
    register_response = requests.post('http://localhost:8000/api/v1/register/', data=register_data)
    print(f"Register status: {register_response.status_code}")
    
    if register_response.status_code == 200:
        tokens = register_response.json()
        access_token = tokens['access_token']
        print(f"Access token: {access_token}")
        
        # Now test creating a price record with the token
        price_data = {
            "work_type_children_id": 2,
            "price": 2000.0
        }
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Test creating price record
        price_response = requests.post(
            'http://localhost:8000/api/v1/price/', 
            json=price_data,
            headers=headers
        )
        print(f"Price create status: {price_response.status_code}")
        print(f"Price create response: {price_response.json()}")
        
        # Test getting price record
        get_response = requests.get(
            'http://localhost:8000/api/v1/price/2',
            headers=headers
        )
        print(f"Price get status: {get_response.status_code}")
        print(f"Price get response: {get_response.json()}")
        
    else:
        print(f"Registration failed: {register_response.json()}")
        
except Exception as e:
    print(f"Error: {e}")