config_templates/
│── customers.json
│── template_groups.json
│── templates/
│   │── cisco_router_template.j2
│   │── cisco_switch_template.j2
│── configs/
│   │── ABC_Corp/
│   │   │── core_router_config.json
│   │   │── access_switch_config.json
│   │── XYZ_Tech/
│   │   │── branch_router_config.json
│   │   │── distribution_switch_config.json

3. Meaningful Customer & Device Names
Customer Name	Device Type	            Device Name	                Config File
ABC_Corp	    Core Router	            Core_Router	            core_router_config.json
ABC_Corp	    Access Switch	        Access_Switch	        access_switch_config.json
XYZ_Tech	    Branch Router	        Branch_Office_Router	branch_router_config.json
XYZ_Tech	    Distribution Switch	    Distribution_Switch	    distribution_switch_config.json


# Task: For configs collection I wanted to build endpoints to do CRUD operations
## Implimentation details
1. the configs collectins will have below columns
    _id, name, customer, config_data, create_by, created_at, status
2. name: is the key to do all CRUD operations - Manadotory parameter
3. customer: Is the customer name which should be part of customers.name collection - Manadotory parameter
4. The two parameaters (name, customer) are query level parameters
5. config_data: os JSON object which is passed as part of Body - Manadotory parameter
6. end_points to create
    create_config
        config-name
        customer
        config_data

    create_config_by_file
        config-name
        customer
        config file attach

    list_configs
        list all configs

    list_configs_by_customer
        list all configs by customer name

    list_configs_by_user
        list all configs by user name

    update_config : Parameters 
        config-name
        new-config-name
        customer
        config_data

    delete_config
        config-name
7. Generate models.py and schemas.py
8. Generate only changes to keep in initialize_permissions.py
9. Define router file content is like below
    router = APIRouter()
    @router.get
10. Continue to use authentication and authraization as there in customers_router.py


# Task: I want to make changes to configs collection
## Changes
1. Remove column customer from the schema
2. Add a new column device_name
    Note: Device name is foregin key to devices.name
6. end_points to create
    create_config
        config-name - Mandotory field
        device_name - Mandotory field
        config_data - Mandotory field

    create_config_by_file
        config-name - Mandotory field
        device_name - Mandotory field
        config file attach - Mandotory field

    list_configs - No changes
    list_configs_by_customer
        list all configs by configs.devices_name == devices.name -> devices.customer_name

    list_configs_by_user - No changes

    update_config : Parameters 
        config-name - Mandotory field
        new-config-name - Mandotory field
        device_name - optional
        config_data - optional

    delete_config - No changes

7. Generate models.py and schemas.py if changes required
8. Generate only changes to keep in initialize_permissions.py
9. Define router file content is like below
    router = APIRouter()
    @router.get
10. Continue to use authentication and authraization as there in customers_router.py


<!-- ######################################## -->

# Task: I want to write a endpoint to generate the configuration file with the help of LLM
## Note: Refer config_to_template function in generate_configuration.py file

# Input: 
## Device information: devices.name -> "Core_Router"
## Template details: template.template_name -> "cisco_router_template"
## Config Values: config_values.name -> "core_router_config"

# output:
## A new document to be added to configs collection with below values (<customer>_<device_type>_<device_name>_<location>)
    _id: <system generated>
    name: <devices.customer_name>_<devices.type>_<devices.name>_<devices_location>_cfg
    device_name: <devices.name>
    config_data: <Generated configuration data>
    created_by: <user name>
    created_at: <time stamp>
    status: "active"

# Instructions
1. end points to create - create_configuration
    device_name - Mandotory field
    config_template_name - Mandotory field
    config_values_name - Mandotory field

2. Generate models.py and schemas.py if changes required
3. Generate only changes to keep in initialize_permissions.py
4. Define router file content is like below
    router = APIRouter()
    @router.get
5. Continue to use authentication and authraization as there in customers_router.py
6. The return value from end point is
    ** configuration Name **
    document.name

    ** configuration data **
    document.config_data in redable multilined plain text




# Task: I want to write below endpoints on configs collections

# End point details and Instructions
## 1. List all documents in the collections
    Input : Nothing
## 2. List all configs in the collection based on configs.name
    Input : name of the config
## 3. List all configs in the collection created by a specific user
    Input : name of the user
## 4. Delete the document from the collection based on configs.name
    Input : name of the config
## 5. Define router file content is like below
    router = APIRouter()
    @router.get
## 5. Continue to use authentication and authraization as there in customers_router.py
## 7. Generate only changes to keep in initialize_permissions.py

# Task: Now I want to add one more endpoin to edit the contiguration in configs collections

# End point details and Instructions
## Edit the configuraion of collection based name of the config
    Input : name of the config
    name - Mandotory field
    new-name - Mandotory field
    config_data - optional, if nothing is given the existing value should be retained
## 5. Define router file content is like below
    router = APIRouter()
    @router.get
## 5. Continue to use authentication and authraization as there in customers_router.py
## 7. Generate only changes to keep in initialize_permissions.py
