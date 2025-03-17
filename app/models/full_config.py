# app/models/full_config_model.py

from typing import Dict, Optional
from pydantic import BaseModel

class FullConfigModel(BaseModel):
    customer_name: str
    vrf_data: Dict
    interface_data: Dict
    subinterface_data: Dict
    global_bgp_data: Dict
    local_bgp_data: Dict