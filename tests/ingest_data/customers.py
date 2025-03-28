# tests/ingest_data/customers.py

import requests
import json

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

def list_customers(base_url, access_token):
    """Lists all customer names."""
    url = f"{base_url}/customers/"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        print("\n--- Customers ---")
        for item in data:
            name = item.get("name")
            if name:
                print(f"- {name}")
            else:
                print(f"- (Name not found in item: {item})")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching customers: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response for customers")