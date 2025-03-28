# tests/ingest_data/ingest_data.py

from settings import ingest_settings
from login import get_access_token
from customers import add_customer
from devices import add_device
from templates import add_template
from config_values import add_config_value
import json


def ingest_data():
    base_url = ingest_settings.BASE_URL

    username = ingest_settings.USERNAME
    password = ingest_settings.PASSWORD

    access_token = get_access_token(base_url, username, password)

    if not access_token:
        print("Failed to obtain access token.  Cannot add customers.")
        
    try:  
        add_customer(base_url, "ABC_Corp", access_token)
        add_customer(base_url, "XYZ_Tech", access_token)
    except Exception as e:
        print("Adding customer failed")
        return
        
    try:
        add_device(base_url, "ABC_Corp", "Core_Router", "router", "HQ - Data Center", access_token)
        add_device(base_url, "ABC_Corp", "Access_Switch", "switch", "HQ - Data Center", access_token)
    except Exception as e:
        print("Adding ABC_Corp Device failed")
        return

    try:
        add_device(base_url, "XYZ_Tech", "Branch_Office_Router", "router", "Branch Office - New York", access_token)
        add_device(base_url, "XYZ_Tech", "Distribution_Switch", "switch", "Branch Office - New York", access_token)
    except Exception as e:
        print("Adding XYZ_Tech Device failed")
        return


    # Read template content from file
    try:
        with open("cisco_router_template.j2", "r") as f:
            template_content = f.read()
    except FileNotFoundError:
        print("Error: cisco_router_template.j2 not found.")
        return  # Or raise an exception

    try:
        add_template(base_url, "cisco_router_template", template_content, access_token)
    except Exception as e:
        print("Adding add_template failed")
        return

    # Read config values from file
    try:
        with open("core_router_config.json", "r") as f:
            config_data = json.load(f)
    except FileNotFoundError:
        print("Error: core_router_config.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON in core_router_config.json")
        return

    try:
        add_config_value(base_url, "core_router_config", "Branch_Office_Router", config_data, access_token)    
    except Exception as e:
        print("Adding core_router_config failed")
        return
                       
if __name__ == "__main__":
    ingest_data()
