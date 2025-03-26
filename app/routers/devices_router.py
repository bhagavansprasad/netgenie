from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.core.database import get_database
from app.models.devices_model import DeviceDetails
from app.core.auth import check_permission
from datetime import datetime
from app.schemas.user_schemas import UserResponse
from app.core.security import get_current_user
from pymongo import ReturnDocument

router = APIRouter()

@router.post("/devices/", response_model=DeviceDetails, status_code=201,
          dependencies=[Depends(check_permission)], name="create_device")
async def create_device(
    customer_name: str = Query(..., description="Customer name"),
    name: str = Query(..., description="Device name"),
    type: str = Query(..., description="Device type (router/switch)"),
    location: str = Query(..., description="Device location"),
    db = Depends(get_database),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Creates a new device.
    """
    # Before inserting, check if the device_id already exists
    device_id = f"{customer_name}-{name}".replace(" ", "_") # Create device_id
    if await db["devices"].find_one({"device_id": device_id}):
        raise HTTPException(status_code=400, detail="Device ID already exists")

    # Verify that the customer name exists in the customers collection
    customer = await db["customers"].find_one({"name": customer_name})
    if not customer:
        raise HTTPException(status_code=400, detail="Customer name does not exist")


    # Create the device object. Status is defaulted to active.
    device = DeviceDetails(customer_name=customer_name, device_id=device_id, name=name, type=type, location=location, status="active", created_by=current_user.username, timestamp=datetime.now())
    device_dict = device.model_dump(exclude={"id"})  # Exclude id as MongoDB will generate it
    result = await db["devices"].insert_one(device_dict)
    new_device = await db["devices"].find_one({"_id": result.inserted_id})

    # Convert ObjectId to string before creating the DeviceDetails object
    new_device["_id"] = str(new_device["_id"])

    return DeviceDetails(**new_device)

@router.get("/devices/", response_model=List[DeviceDetails],
         dependencies=[Depends(check_permission)], name = "list_devices")
async def list_devices(db = Depends(get_database)):
    """
    Lists all devices.
    """
    devices = []
    async for device in db["devices"].find():
        device["_id"] = str(device["_id"])  # Convert ObjectId to string
        devices.append(DeviceDetails(**device))
    return devices

@router.get("/devices/{name}", response_model=DeviceDetails,
         dependencies=[Depends(check_permission)], name = "read_device")
async def read_device(name: str, db = Depends(get_database)):
    """
    Reads a device by device name.
    """
    device = await db["devices"].find_one({"name": name})
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    device["_id"] = str(device["_id"])
    return DeviceDetails(**device)

@router.put("/devices/{name}", response_model=DeviceDetails,
            dependencies=[Depends(check_permission)], name="update_device")
async def update_device(
    name: str,  # Existing device name
    new_name: Optional[str] = Query(
        None, description="New Device name. If not provided, existing name is retained"
    ),
    customer_name: Optional[str] = Query(None, description="Customer name"),
    type: Optional[str] = Query(None, description="Device type (router/switch)"),
    location: Optional[str] = Query(None, description="Device location"),
    db=Depends(get_database),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Updates a device's details based on the existing device name.
    Provides the option to change the device name.
    If other values are not provided, existing values are retained.
    """
    # Before updating, check if the device exists with the existing device name
    existing_device = await db["devices"].find_one({"name": name})
    if not existing_device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Assign new values or retain existing values
    new_customer_name = (
        customer_name
        if customer_name is not None
        else existing_device["customer_name"]
    )
    new_type = type if type is not None else existing_device["type"]
    new_location = location if location is not None else existing_device["location"]
    new_device_name = new_name if new_name is not None else existing_device["name"]

    # Verify the new_customer_name.  Moved this check *before* checking `new_name`
    customer = await db["customers"].find_one({"name": new_customer_name})
    if not customer:
        raise HTTPException(
            status_code=400, detail="Customer name does not exist"
        )

    # If a new name is provided AND it's different from the *existing* name, *then*
    # check if that new name already exists.  The crucial check `new_device_name != name`
    # prevents a false positive when the user isn't *actually* trying to rename.
    if new_name and new_device_name != name:
        if await db["devices"].find_one({"name": new_device_name}):
            raise HTTPException(
                status_code=400, detail="New device name already exists"
            )

    # Update the device object
    device_id = f"{new_customer_name}-{new_device_name}".replace(
        " ", "_"
    )  # Create device_id
    device_dict = {
        "customer_name": new_customer_name,
        "name": new_device_name,
        "type": new_type,
        "device_id": device_id,
        "location": new_location,
        "status": "active",
        "created_by": current_user.username,
        "timestamp": datetime.now(),
    }

    # Update the DB call. Use `new_device_name` to perform name change, update all other values
    update_result = await db["devices"].update_one(
        {"name": name}, {"$set": device_dict}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Device not found")  # Double check

    # Find device to return, using NEW device name, otherwise it is going to fail.
    updated_device = await db["devices"].find_one({"name": new_device_name})
    if not updated_device:
        raise HTTPException(status_code=404, detail="Device not found after update")

    updated_device["_id"] = str(updated_device["_id"])  # Convert Object ID
    return DeviceDetails(**updated_device)


@router.delete("/devices/{name}", status_code=204,
           dependencies=[Depends(check_permission)], name="delete_device")
async def delete_device(name: str, db = Depends(get_database)):
    """
    Deletes a device by device name.
    """
    delete_result = await db["devices"].delete_one({"name": name})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Device not found")
    return None


@router.put(
    "/devices/{name}/rename",
    response_model=DeviceDetails,
    dependencies=[Depends(check_permission)],
    name="rename_device",
)
async def rename_device(
    name: str,  # Existing device name
    new_name: str = Query(..., description="New Device name."),
    db=Depends(get_database),
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Renames a device, based on the existing device name.
    """
    # Before renaming, check if the device exists with the existing device name
    existing_device = await db["devices"].find_one({"name": name})
    if not existing_device:
        raise HTTPException(status_code=404, detail="Device not found")

    if await db["devices"].find_one({"name": new_name}):
        raise HTTPException(status_code=400, detail="New device name already exists")

    customer_name = existing_device[
        "customer_name"
    ]  # Get existing customer name
    device_id = f"{customer_name}-{new_name}".replace(
        " ", "_"
    )  # Create device_id

    device_dict = {
        "customer_name": customer_name,
        "name": new_name,
        "type": existing_device["type"],
        "device_id": device_id,
        "location": existing_device["location"],
        "status": existing_device["status"],
        "created_by": current_user.username,
        "timestamp": datetime.now(),
    }

    update_result = await db["devices"].update_one(
        {"name": name}, {"$set": device_dict}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Device not found")

    updated_device = await db["devices"].find_one({"name": new_name})
    if not updated_device:
        raise HTTPException(status_code=404, detail="Device not found after rename")

    updated_device["_id"] = str(updated_device["_id"])
    return DeviceDetails(**updated_device)

# Additional endpoints for filtering

@router.get("/devices/by-customer/{customer_name}", response_model=List[DeviceDetails],
         dependencies=[Depends(check_permission)], name="get_devices_by_customer")
async def get_devices_by_customer(customer_name: str, db = Depends(get_database)):
    """
    Get devices by customer name.
    """
    devices = []
    async for device in db["devices"].find({"customer_name": customer_name}):
        device["_id"] = str(device["_id"])
        devices.append(DeviceDetails(**device))
    return devices

@router.get("/devices/by-type/{device_type}", response_model=List[DeviceDetails],
         dependencies=[Depends(check_permission)], name="get_devices_by_type")
async def get_devices_by_type(device_type: str, db = Depends(get_database)):
    """
    Get devices by device type.
    """
    devices = []
    async for device in db["devices"].find({"type": device_type}):
        device["_id"] = str(device["_id"])
        devices.append(DeviceDetails(**device))
    return devices

@router.get("/devices/by-location/{location}", response_model=List[DeviceDetails],
         dependencies=[Depends(check_permission)], name="get_devices_by_location")
async def get_devices_by_location(location: str, db = Depends(get_database)):
    """
    Get devices by location.
    """
    devices = []
    async for device in db["devices"].find({"location": location}):
        device["_id"] = str(device["_id"])
        devices.append(DeviceDetails(**device))
    return devices

@router.get("/devices/by-status/{status}", response_model=List[DeviceDetails],
         dependencies=[Depends(check_permission)], name="get_devices_by_status")
async def get_devices_by_status(status: str, db = Depends(get_database)):
    """
    Get devices by status.
    """
    devices = []
    async for device in db["devices"].find({"status": status}):
        device["_id"] = str(device["_id"])
        devices.append(DeviceDetails(**device))
    return devices

@router.get("/devices/by-creator/{created_by}", response_model=List[DeviceDetails],
         dependencies=[Depends(check_permission)], name="get_devices_by_creator")
async def get_devices_by_creator(created_by: str, db = Depends(get_database)):
    """
    Get devices by creator (username).
    """
    devices = []
    async for device in db["devices"].find({"created_by": created_by}):
        device["_id"] = str(device["_id"])
        devices.append(DeviceDetails(**device))
    return devices
