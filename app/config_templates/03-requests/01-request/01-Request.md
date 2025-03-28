### **Request from Network Architect to Network Engineer**  

**Subject:** Configuration Request for New Core Router Deployment – ABC_Corp  

**Dear [Network Engineer's Name],**  

We need to deploy a **Core Router** for **ABC_Corp** following our standard configuration policies. Below are the details you need to generate the configuration using the appropriate template.  

---

### **1️⃣ Device Information**  
- **Customer:** ABC_Corp  
- **Device Name:** Core_Router  
- **Device Type:** Router  
- **Location:** Data Center - New York  
- **Status:** Active  

---

### **2️⃣ Template Information**  
- **Template Path:** `app/config_templates/templates/`  
- **Template File:** `cisco_router_template.j2`  

---

### **3️⃣ Configuration File Details**  
- **Config Path:** `app/config_templates/configs/ABC_Corp/`  
- **Config File:** `core_router_config.json`  

---

### **4️⃣ Configuration Values to Use**  
```json
{
    "hostname": "CORE-RTR-001",
    "interfaces": {
        "GigabitEthernet0/0": {
            "ip_address": "192.168.1.1",
            "subnet_mask": "255.255.255.0",
            "description": "Uplink to ISP"
        },
        "GigabitEthernet0/1": {
            "ip_address": "10.1.1.1",
            "subnet_mask": "255.255.255.0",
            "description": "Internal Network"
        }
    },
    "routing": {
        "ospf": {
            "process_id": 1,
            "networks": [
                {
                    "network": "192.168.1.0",
                    "wildcard_mask": "0.0.0.255",
                    "area": 0
                },
                {
                    "network": "10.1.1.0",
                    "wildcard_mask": "0.0.0.255",
                    "area": 0
                }
            ]
        }
    },
    "security": {
        "ssh": {
            "enabled": true,
            "users": [
                {
                    "username": "admin",
                    "password": "securepassword",
                    "privilege": 15
                }
            ]
        },
        "acl": [
            {
                "name": "ALLOW_INTERNAL",
                "rules": [
                    {
                        "action": "permit",
                        "protocol": "ip",
                        "source": "10.1.1.0",
                        "destination": "any"
                    }
                ]
            }
        ]
    }
}
```

---

### **5️⃣ Next Steps**  
1. Use the above **config values** with the **Jinja2 template** (`cisco_router_template.j2`) to generate the final configuration.  
2. Validate the generated config against network policies.  
3. Apply the configuration to the Core Router.  
4. Provide a summary report after the configuration is pushed.  

Let me know if you need any clarifications.  

**Best regards,**  
[Network Architect's Name]  
(Network Architect, ABC_Corp)