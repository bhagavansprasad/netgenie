# tests/create_configuration/create_configuration.py

import requests
from settings import ingest_settings  # Assuming you have BASE_URL and AUTH_TOKEN there.  Adjust if necessary.

def create_configuration(device_name, config_template_name, config_values_name, access_token):
    """
    Creates a configuration by making a POST request to the configurations endpoint.

    Args:
        device_name (str): The name of the device.
        config_template_name (str): The name of the configuration template.
        config_values_name (str): The name of the configuration values.
        access_token (str): The access token for authentication.

    Returns:
        bool: True if the configuration was created successfully, False otherwise.
    """

    base_url = ingest_settings.BASE_URL  # Get the base URL from settings.

    url = f"{base_url}/configurations/?device_name={device_name}&config_template_name={config_template_name}&config_values_name={config_values_name}"
    headers = {
        'accept': 'text/plain',  # Or 'application/json' based on what the server returns
        'Authorization': f'Bearer {access_token}'
    }
    data = ''  # No data in the body

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        print(f"Configuration created successfully.  Status code: {response.status_code}")  # Add success message
        return True  # Indicate success
    except requests.exceptions.RequestException as e:
        print(f"Error creating configuration: {e}") # Add error message with exception info
        return False   # Indicate failure


if __name__ == '__main__':
    # Example usage (replace with your actual values)
    from login import get_access_token  # Import get_access_token

    base_url = ingest_settings.BASE_URL
    username = ingest_settings.USERNAME
    password = ingest_settings.PASSWORD

    access_token = get_access_token(base_url, username, password)

    device_name = "Core_Router"
    config_template_name = "cisco_router_template"
    config_values_name = "core_router_config"

    if access_token:
        success = create_configuration(device_name, config_template_name, config_values_name, access_token)
        if success:
            print("Configuration creation process completed.")
        else:
            print("Configuration creation process failed.")
    else:
        print("Failed to retrieve access token. Cannot create configuration.")
        