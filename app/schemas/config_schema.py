from pydantic import BaseModel
from typing import Optional

class NetworkConfig(BaseModel):
    hostname: str
    interface_name: str
    ip_address: str
    subnet_mask: str
    description: Optional[str] = "Default Interface"
