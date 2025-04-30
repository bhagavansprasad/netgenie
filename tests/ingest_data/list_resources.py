# tests/ingest_data/ingest_data.py

from settings import ingest_settings
from login import get_access_token
from customers import list_customers
from devices import list_devices
from templates import list_config_templates
from config_values import list_config_values


def list_resources():
    base_url = ingest_settings.BASE_URL

    username = ingest_settings.USERNAME
    password = ingest_settings.PASSWORD

    access_token = get_access_token(base_url, username, password)

    if not access_token:
        print("Failed to obtain access token.  Cannot add customers.")

    """Main function to orchestrate the listing of resources."""
    username = ingest_settings.USERNAME
    password = ingest_settings.PASSWORD

    access_token = get_access_token(base_url, username, password)

    if not access_token:
        print("Failed to obtain access token.  Cannot list resources.")
        return

    list_customers(base_url, access_token)
    list_devices(base_url, access_token)
    list_config_templates(base_url, access_token)
    list_config_values(base_url, access_token)

def main():
    list_resources()    
                           
if __name__ == "__main__":
    main()
