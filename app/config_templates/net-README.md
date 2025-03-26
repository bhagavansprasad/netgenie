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