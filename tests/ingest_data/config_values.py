# tests/ingest_data/config_values.py

import requests
import json

def add_config_value(base_url, name, device_name, config_data, access_token):
    """Adds a config value to the database using the API."""
    config_values_url = f"{base_url}/config_values/?name={name}&device_name={device_name}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(config_values_url, headers=headers, data=json.dumps(config_data))
        response.raise_for_status()
        print(f"Config value '{name}' added successfully for device '{device_name}'.")
        print(f"Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error adding config value '{name}' for device '{device_name}': {e}")

def list_config_values(base_url, access_token):
    """Lists all config value names."""
    url = f"{base_url}/config_values/"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        print("\n--- Config Values ---(config_values.name)")
        for item in data:
            name = item.get("name")
            if name:
                print(f"- {name}")
            else:
                print(f"- (Name not found in item: {item})")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching config values: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response for config values")
