from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.core.database import get_database
from app.models.customer_model import Customer #Import the models
from app.core.auth import check_permission #Import the auth dependencies
from datetime import datetime
from app.schemas.user_schemas import UserResponse #Import UserResponse
from app.core.security import get_current_user # Import the get_current_user

router = APIRouter()

@router.post("/customers/", response_model=Customer, status_code=201,
          dependencies=[Depends(check_permission)], name="create_customer")
async def create_customer(
    customer_name: str = Query(..., description="Name of the customer to create"),
    db = Depends(get_database),
    current_user: UserResponse = Depends(get_current_user)
    ):
    """
    Creates a new customer.  Only customer_name is required as a query parameter.
    """
    # Before inserting check if customer name already exists
    if await db["customers"].find_one({"name": customer_name}):
        raise HTTPException(status_code=400, detail="Customer name already exists")

    #Create the customer object
    customer = Customer(name=customer_name, created_by=current_user.username, timestamp=datetime.now())
    customer_dict = customer.model_dump(exclude={"id"}) # Exclude id as MongoDB will generate it
    result = await db["customers"].insert_one(customer_dict)
    new_customer = await db["customers"].find_one({"_id": result.inserted_id})

    # Convert ObjectId to string before creating the Customer object
    new_customer["_id"] = str(new_customer["_id"])

    return Customer(**new_customer)  # Return the validated object


@router.get("/customers/", response_model=List[Customer],
         dependencies=[Depends(check_permission)])
async def list_customers(db = Depends(get_database)):
    """
    Lists all customers.
    """
    customers = []
    async for customer in db["customers"].find():
        customer["_id"] = str(customer["_id"])  # Convert ObjectId to string
        customers.append(Customer(**customer))
    return customers

@router.get("/customers/by-name/{customer_name}", response_model=Customer,
         dependencies=[Depends(check_permission)], name = "read_customer_by_name")
async def read_customer_by_name(customer_name: str, db = Depends(get_database)):
    """
    Reads a customer by name.
    """
    customer = await db["customers"].find_one({"name": customer_name})
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer["_id"] = str(customer["_id"]) #Convert object ID
    return Customer(**customer)


@router.put("/customers/by-name/{old_customer_name}", response_model=Customer,
          dependencies=[Depends(check_permission)], name = "update_customer_by_name")
async def update_customer_by_name(
    customer_name: str,
    new_customer_name: str = Query(..., description="New name for the customer"),
    db = Depends(get_database),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Updates a customer's name based on the existing customer name.
    Requires the existing customer name as a path parameter and the new customer name as a query parameter.
    """
    # Before updating, check if the customer exists with the old name
    existing_customer = await db["customers"].find_one({"name": customer_name})
    if not existing_customer:
        raise HTTPException(status_code=404, detail="Customer not found with the specified name")
    
    # Check for duplicate customer name, excluding the current customer
    if await db["customers"].find_one({"name": new_customer_name, "_id": {"$ne": existing_customer['_id']}}):
        raise HTTPException(status_code=400, detail="Customer name already exists")

    #Update the customer object
    customer_dict = {"name": new_customer_name, "created_by": current_user.username, "timestamp": datetime.now()} #Exclude ID and update only values
    update_result = await db["customers"].update_one({"name": customer_name}, {"$set": customer_dict}) #Update the DB call.

    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found")  #Double check

    updated_customer = await db["customers"].find_one({"name": new_customer_name}) #Find customer to return
    updated_customer["_id"] = str(updated_customer["_id"]) #Convert Object ID
    return Customer(**updated_customer)


@router.delete("/customers/by-name/{customer_name}", status_code=204,
           dependencies=[Depends(check_permission)], name="delete_customer_by_name")
async def delete_customer_by_name(customer_name: str, db = Depends(get_database)):
    """
    Deletes a customer by name.
    """
    delete_result = await db["customers"].delete_one({"name": customer_name})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return None