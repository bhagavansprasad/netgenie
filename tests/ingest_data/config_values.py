# tests/ingest_data/config_values.py

import requests

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