# app/ai/ai-interface.py
import os
import logging
import json
import re
import jinja2
from typing import Dict, List

from app.ai import common  # Import the common functions
from app.core.settings import settings
from app.ai.common import get_config_content, _render_jinja2_template
from app.ai.common import parse_gentemplate_output
from app.ai.common import parse_genconfig_output

logger = logging.getLogger(__name__)

def config_to_j2_n_json(config: str, prompt_file_path: str = None) -> dict:
    """
    Generates a Jinja2 template and JSON variables from a network configuration
    using a prompt template and an LLM.

    Args:
        config: The network configuration string.
        prompt_file_path: The path to the prompt template file.

    Returns:
        A dictionary containing the Jinja2 template and JSON variables, or an error message.
    """
    logger.info(f"Entering config_to_j2_n_json")
    logger.debug(f"Prompt File Path: {prompt_file_path}")
    logger.debug(f"Input config: {config}")


    try:
        prompt_file = prompt_file_path or settings.CONFIG_TO_J2_PROMPT
        logger.debug(f"Using prompt file: {prompt_file}")

        with open(prompt_file, "r") as f:
            prompt_template = f.read()
        logger.debug(f"Prompt template read successfully from {prompt_file}")


        prompt = prompt_template.format(network_config=config)
        logger.debug(f"Prompt after formatting: {prompt}")


        llm_output = common.call_llm_chat(prompt)
        logger.debug(f"LLM Output: {llm_output}")

        data_dict, extracted_data = parse_gentemplate_output(llm_output)
        logger.debug(f"Extracted data after parsing: {extracted_data}")


        if "error" in extracted_data:
            logger.error(f"LLM Error: {extracted_data['error']}")
            return extracted_data

        return data_dict, extracted_data

    except FileNotFoundError:
        error_message = f"Prompt file not found: {prompt_file_path}"
        logger.error(error_message)
        return {"error": error_message}
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        logger.exception(error_message)
        return {"error": error_message}
    finally:
        logger.info("Exiting config_to_j2_n_json")


def j2_and_json_to_config(j2_template: str, json_data: dict, prompt_file_path: str = None) -> dict:
    """
    Generates a Cisco IOS configuration from a Jinja2 template and JSON variables
    using a prompt template and an LLM. The template rendering is performed by the LLM.
    """
    logger.info(f"Entering j2_and_json_to_config")
    logger.debug(f"j2_template: {j2_template}")
    logger.debug(f"json_data: {json_data}")
    logger.debug(f"prompt_file_path: {prompt_file_path}")


    try:
        prompt_file = prompt_file_path or settings.J2_TO_CONFIG_PROMPT
        logger.debug(f"Using prompt file: {prompt_file}")


        with open(prompt_file, "r") as f:
            prompt_template_string = f.read() # Read the prompt template as a string
        logger.debug(f"Prompt template read successfully from {prompt_file}")


        env = jinja2.Environment()
        prompt_template = env.from_string(prompt_template_string)
        prompt = prompt_template.render(j2_template=j2_template, json_data=json_data) # Use Jinja2 render
        logger.debug(f"Prompt after rendering: {prompt}")


        llm_output = common.call_llm_chat(prompt)
        logger.debug(f"LLM Output: {llm_output}")


        extracted_data = parse_genconfig_output(llm_output)
        logger.debug(f"Extracted data after parsing: {extracted_data}")


        if "error" in extracted_data:
            logger.error(f"LLM output Error: {extracted_data}")
            return extracted_data

        if 'message' in extracted_data and 'config' in extracted_data['message']:
            logger.info(f"Generated config length: {len(extracted_data['message']['config'])}")
        return {"message": extracted_data}

    except FileNotFoundError:
        error_message = f"Prompt file not found: {prompt_file_path}"
        logger.error(error_message)
        return {"error": error_message}

    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        logger.exception(error_message)
        return {"error": error_message}
    finally:
        logger.info("Exiting j2_and_json_to_config")

def generate_complete_config(
    customer_name: str,
    vrf_data: Dict,
    interface_data: Dict,
    subinterface_data: Dict,
    global_bgp_data: Dict,
    local_bgp_data: Dict,
) -> dict:
    """
    Generates a complete Cisco IOS configuration from various JSON data inputs.
    This function orchestrates the generation of the full configuration.
    """
    logger.info("Entering generate_complete_config")
    logger.debug(f"customer_name: {customer_name}")
    logger.debug(f"vrf_data: {vrf_data}")
    logger.debug(f"interface_data: {interface_data}")
    logger.debug(f"subinterface_data: {subinterface_data}")
    logger.debug(f"global_bgp_data: {global_bgp_data}")
    logger.debug(f"local_bgp_data: {local_bgp_data}")

    template_data = {
        "vrf": "app/netconfigs/templates/j2/01-vrf.j2",
        "interface": "app/netconfigs/templates/j2/02-interface.j2",
        "subinterface": "app/netconfigs/templates/j2/03-subinterface.j2",
        "bgp_global": "app/netconfigs/templates/j2/04-bgp-global.j2",
        "bgp_local": "app/netconfigs/templates/j2/05-bgp-local.j2",
    }

    try:
        template_contents = {}
        for config_type, template_path in template_data.items():
            with open(template_path, "r") as f:
                template_contents[config_type] = f.read()
            # logger.debug(f"Template read successfully from {template_path}")


        logger.debug("-------------")
        logger.debug(f"template_contents :\n{template_contents}")
        logger.debug("-------------")
        # Load Prompt
        prompt_file_path = "app/ai/prompts/full-config.prompt"
        with open(prompt_file_path, "r") as f:
            prompt_template = f.read()
        logger.debug(f"Prompt template read successfully from {prompt_file_path}")

        logger.debug(f"prompt_template before formatting: {prompt_template}")
        # Prepare arguments for prompt
        prompt_args = {
            "vrf_j2_template": template_contents["vrf"],
            "interface_j2_template": template_contents["interface"],
            "sub_interface_j2_template": template_contents["subinterface"],
            "bgp_global_j2_template": template_contents["bgp_global"],
            "bgp_local_j2_template":  template_contents["bgp_local"],
        }

        # Format the prompt
        prompt = prompt_template.format(
            customer_name             = customer_name,
            vrf_j2_template           = prompt_args['vrf_j2_template'],
            vrf_json_data             = json.dumps(vrf_data, indent=4),
            interface_j2_template     = prompt_args['interface_j2_template'],
            interface_json_data       = json.dumps(interface_data, indent=4),
            sub_interface_j2_template = prompt_args['sub_interface_j2_template'],
            sub_interface_json_data   = json.dumps(subinterface_data, indent=4),
            bgp_global_j2_template    = prompt_args['bgp_global_j2_template'],
            bgp_global_json_data      = json.dumps(global_bgp_data, indent=4),
            bgp_local_j2_template     = prompt_args['bgp_local_j2_template'],
            bgp_local_json_data       = json.dumps(local_bgp_data, indent=4),
            )
        logger.debug(f"Prompt after formatting: {prompt}")

        # Call LLM and parse the output
        llm_output = common.call_llm_chat(prompt)
        extracted_data = parse_genconfig_output(llm_output)
        logger.debug(f"Extracted data after parsing: {extracted_data}")

        full_config = extracted_data

        logger.info("Successfully generated full configuration.")
        return {"config": full_config}

    except Exception as e:
        error_message = f"Error generating complete configuration: {e}"
        logger.exception(error_message)
        return {"error": error_message}
    finally:
        logger.info("Exiting generate_complete_config")


def test_generate_complete_config():
    customer_name = "cust202"
    vrf_data = {
        "vrf_name": "CUST101",
        "vrf_description": "Customer 101 VRF",
        "rt_export": "101:101",
        "rt_import": "101:101"
    }
    interface_data = {
        "interface_name": "GigabitEthernet0/0/0/1",
        "description": "Customer 101 Uplink",
        "mtu": 9216
    }
    subinterface_data = {
        "interface_name": "GigabitEthernet0/0/0",
        "subinterface_vlan": "101",
        "description": "Sub-interface for Customer 101",
        "vrf": "CUST101",
        "ipv4_address": "192.168.101.1",
        "subnet_mask": "255.255.255.0",
        "ipv6_address": "2001:db8:101::1/64"
    }
    global_bgp_data = {
        "bgp_asn": "65001",
        "router_id": "1.1.1.1",
        "ipv4_network_1": "10.0.0.0/8",
        "ipv4_network_2": "192.168.101.0/24",
        "ipv6_network": "2001:db8:101::/64"
    }
    local_bgp_data = {
        "asn": "65001",
        "vrf_name": "CUST101",
        "rd": "101:101"
    }

    generate_complete_config(
        customer_name,
        vrf_data,
        interface_data,
        subinterface_data,
        global_bgp_data,
        local_bgp_data
        )

# import logging
# format = '%(name)s:%(lineno)d: %(message)s'
# logging.basicConfig(level=logging.DEBUG, format=format)
# logger = logging.getLogger(__name__)
# if __name__ == "__main__":
#     logger.debug("Hello world")
#     test_generate_complete_config()
    