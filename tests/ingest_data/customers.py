# tests/ingest_data/customers.py

import requests

def add_customer(base_url, customer_name, access_token):
    """Adds a customer to the database using the API."""
    customers_url = f"{base_url}/customers/?customer_name={customer_name}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.post(customers_url, headers=headers)
        response.raise_for_status()
        print(f"Customer '{customer_name}' added successfully.")
        print(f"Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error adding customer '{customer_name}': {e}")
