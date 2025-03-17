import json

# Define variables separately
customer_name = "cust_202"

vrf_j2_template = """
vrf { vrf_name }
 description { vrf_description }
"""

vrf_json_data = {
    "vrf_name": "CUST101",
    "vrf_description": "Customer 101 VRF",
    "rt_export": "101:101",
    "rt_import": "101:101"
}

# Define the prompt template separately
prompt_template = """
1. **Output Format:**
   - Add a hostname to the device

### **Input Data:**

#### **Customer Name:**
{customer_name}

#### **VRF Jinja2 Template:**
{vrf_j2_template}

#### **VRF JSON Variables:**
{vrf_json_data}
"""

# Fill the template using format()
filled_prompt = prompt_template.format(
    customer_name=customer_name,
    vrf_j2_template=vrf_j2_template.strip(),  
    vrf_json_data=json.dumps(vrf_json_data, indent=2)
)

print(filled_prompt)
