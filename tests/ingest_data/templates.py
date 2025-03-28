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
