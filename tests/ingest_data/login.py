# tests/ingest_data/login.py

import requests
from settings import ingest_settings

def get_access_token(base_url, username, password):
    """
    Authenticates a user and retrieves an access token from the FastAPI backend.

    Args:
        base_url (str): The base URL of the API.
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        str: The access token if authentication is successful, otherwise None.
    """

    token_url = f"{base_url}/auth/login"

    form_data = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(token_url, data=form_data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        token_data = response.json()
        access_token = token_data.get("access_token")
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Error during authentication: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error parsing response: {e}")
        return None


if __name__ == '__main__':
    base_url = ingest_settings.BASE_URL
    username = ingest_settings.USERNAME  # Use the username from ingest_settings
    password = ingest_settings.PASSWORD  # Use the password from ingest_settings
    token = get_access_token(base_url, username, password)
    print(token)
