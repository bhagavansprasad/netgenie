import logging
from app.core.database import get_database

logger = logging.getLogger(__name__)

async def on_startup_db_initialize_permissions():
    db = await get_database()  # Await the coroutine to get the database object
    collection_names = await db.list_collection_names() # Await here
    if "endpoint_permissions" not in collection_names:
        await db.create_collection("endpoint_permissions")
       
    if await db["endpoint_permissions"].count_documents({}) != 0:
        logger.info("Endpoint permissions already initialized.")
        return 
    
    permissions = [
        {
            "endpoint_name": "list_users",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "read_user",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "create_user",
            "role_id": 1,
            "method": "POST"
        },
        {
            "endpoint_name": "update_user",
            "role_id": 1,
            "method": "PUT"
        },
        {
            "endpoint_name": "delete_user",
            "role_id": 1,
            "method": "DELETE"
        },
        {
            "endpoint_name": "list_roles",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "read_role",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "config_to_template",
            "role_id": 1,
            "method": "POST"
        },
        {
            "endpoint_name": "list_templates",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "read_complete_template",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "get_templates_by_criteria",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "update_template",
            "role_id": 1,
            "method": "PUT"
        },
        {
            "endpoint_name": "delete_template",
            "role_id": 1,
            "method": "DELETE"
        },    
        {
            "endpoint_name": "read_jinja2_template",
            "role_id": 1,
            "method": "GET"
        },    
        {
            "endpoint_name": "create_text_template",
            "role_id": 1,
            "method": "POST"
        },
        {
            "endpoint_name": "create_template_from_file",
            "role_id": 1,
            "method": "POST"
        },
        {
            "endpoint_name": "list_customers",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "read_customer_by_name",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "update_customer_by_name",
            "role_id": 1,
            "method": "PUT"
        },
        {
            "endpoint_name": "delete_customer_by_name",
            "role_id": 1,
            "method": "DELETE"
        },
        {
            "endpoint_name": "create_customer",
            "role_id": 1,
            "method": "POST"
         },
        {
            "endpoint_name": "create_device",
            "role_id": 1,
            "method": "POST"
        },
        {
            "endpoint_name": "list_devices",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "read_device",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "update_device",
            "role_id": 1,
            "method": "PUT"
        },
        {
            "endpoint_name": "delete_device",
            "role_id": 1,
            "method": "DELETE"
        },

        {
            "endpoint_name": "get_devices_by_customer",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "get_devices_by_type",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "get_devices_by_location",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "get_devices_by_status",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "get_devices_by_creator",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "create_config_value",
            "role_id": 1,
            "method": "POST"
        },
        {
            "endpoint_name": "create_config_value_from_file",
            "role_id": 1,
            "method": "POST"
        },
        {
            "endpoint_name": "list_config_values",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "list_config_values_by_customer",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "list_config_values_by_user",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "update_config_value",
            "role_id": 1,
            "method": "PUT"
        },
        {
            "endpoint_name": "delete_config_value",
            "role_id": 1,
            "method": "DELETE"
        },
        {
            "endpoint_name": "create_configuration",
            "role_id": 1,
            "method": "POST"
        },
       {
            "endpoint_name": "list_all_configs",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "read_config_by_name",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "list_configs_by_user",
            "role_id": 1,
            "method": "GET"
        },
        {
            "endpoint_name": "delete_config_by_name",
            "role_id": 1,
            "method": "DELETE"
        },
        {
            "endpoint_name": "update_config_by_name",
            "role_id": 1,
            "method": "PUT"
        },
    ]
    await db["endpoint_permissions"].insert_many(permissions)
    logger.info("Endpoint permissions initialized.")
