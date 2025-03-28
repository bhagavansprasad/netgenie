# tests/ingest_data/devices.py

import requests

def add_device(base_url, customer_name, name, device_type, location, access_token):
    """Adds a device to the database using the API."""
    devices_url = f"{base_url}/devices/?customer_name={customer_name}&name={name}&type={device_type}&location={location}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.post(devices_url, headers=headers)
        response.raise_for_status()
        print(f"Device '{name}' added successfully for customer '{customer_name}'.")
        print(f"Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error adding device '{name}' for customer '{customer_name}': {e}")
        
def list_devices(base_url, access_token):
    """Lists all device names."""
    url = f"{base_url}/devices/"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        print("\n--- Devices ---")
        for item in data:
            name = item.get("name")
            if name:
                print(f"- {name}")
            else:
                print(f"- (Name not found in item: {item})")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching devices: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response for devices")