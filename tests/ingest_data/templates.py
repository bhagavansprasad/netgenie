# tests/ingest_data/templates.py

import requests
def add_template(base_url, template_name, template_content, access_token):
    """Adds a template to the database using the API."""
    templates_url = f"{base_url}/templates/text?template_name={template_name}"
    headers = {
        "accept": "text/plain",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "text/plain"
    }

    try:
        response = requests.post(templates_url, headers=headers, data=template_content)
        response.raise_for_status()
        print(f"Template '{template_name}' added successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error adding template '{template_name}': {e}")

def list_config_templates(base_url, access_token):
    """Lists all config template names."""
    url = f"{base_url}/templates"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        print("\n--- Config Templates ---")
        for item in data:
            name = item.get("template_name")
            if name:
                print(f"- {name}")
            else:
                print(f"- (Name not found in item: {item})")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching config templates: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response for config templates")