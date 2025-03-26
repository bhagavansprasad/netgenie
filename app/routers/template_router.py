from fastapi import APIRouter, HTTPException, Depends, Query, Body
from typing import List, Optional
import logging
from app.core.database import get_database
from bson import ObjectId
from app.schemas.config_schema import ConfigTemplateListResponse, ConfigTemplateResponse
from app.core.auth import check_permission
from pymongo import ReturnDocument
from app.models.config_model import ConfigTemplate
from fastapi.responses import PlainTextResponse

router = APIRouter()

logger = logging.getLogger(__name__)

# 1. List Templates
@router.get("/templates", response_model=List[ConfigTemplateListResponse], name="list_templates",
            dependencies=[Depends(check_permission)])
async def list_templates(db = Depends(get_database)):
    """List all config templates with limited information."""
    logger.info("Entering /templates (GET) endpoint")
    templates = []
    async for template in db["config_templates"].find():
        template["_id"] = str(template["_id"]) # Convert ObjectId to str
        templates.append(ConfigTemplateListResponse(**template)) #convert dict to object
    return templates

# 2. Get by Template Name
@router.get("/templates/{template_name}", response_model=ConfigTemplateResponse, name="read_complete_template",
            dependencies=[Depends(check_permission)])
async def read_complete_template(template_name: str, db = Depends(get_database)):
    """Read a complete config template by its name."""
    logger.info(f"Entering /templates/{template_name} (GET) endpoint")
    template = await db["config_templates"].find_one({"template_name": template_name})
    if template is None:
        raise HTTPException(status_code=404, detail="Template not found")

    template["_id"] = str(template["_id"])  # Convert ObjectId to str

    return ConfigTemplateResponse(**template)


# 3. Get Templates by Username or Device Name
@router.get("/templates", response_model=List[ConfigTemplateListResponse], name="get_templates_by_criteria",
            dependencies=[Depends(check_permission)])
async def get_templates_by_criteria(
    username: Optional[str] = Query(None, description="Filter by username"),
    device_name: Optional[str] = Query(None, description="Filter by device name"),
    db = Depends(get_database)
):
    """
    Get config templates by username or device_name.
    Returns all templates matching the specified criteria. If both username and device_name are None, returns all templates.
    """
    logger.info("Entering /templates (GET) endpoint with query parameters")
    query = {}
    if username:
        query["username"] = username
    if device_name:
        query["device_name"] = device_name

    # Remove the requirement for at least one parameter
    # if not query:
    #    raise HTTPException(status_code=400, detail="Must provide either username or device_name for filtering.")

    templates = []
    async for template in db["config_templates"].find(query):
       templates.append(ConfigTemplateListResponse(**template))
    return templates

# 4. Update Template by Template Name (Allow editing only jinja2_template)
@router.put("/templates/{template_name}", response_class=PlainTextResponse, name="update_template",
            dependencies=[Depends(check_permission)])
async def update_template(
    template_name: str,
    jinja2_template: str = Body(..., media_type="text/plain", description="New Jinja2 template content"),
    db = Depends(get_database)
):
    """Update the jinja2_template of a config template by its name and returns only the updated jinja2_template."""
    logger.info(f"Entering /templates/{template_name} (PUT) endpoint")

    update_result = await db["config_templates"].find_one_and_update(
        {"template_name": template_name},
        {"$set": {"jinja2_template": jinja2_template}},
        return_document=ReturnDocument.AFTER  # to return updated document
    )

    if update_result is None:
        raise HTTPException(status_code=404, detail="Template not found")

    return PlainTextResponse(jinja2_template, media_type="text/plain") # Return as plain text


# 5. Delete Template by Template Name
@router.delete("/templates/{template_name}", status_code=204, name="delete_template",
            dependencies=[Depends(check_permission)])
async def delete_template(template_name: str, db = Depends(get_database)):
    """Delete a config template by its name."""
    logger.info(f"Entering /templates/{template_name} (DELETE) endpoint")
    delete_result = await db["config_templates"].delete_one({"template_name": template_name})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Template not found")
    return None

# 6. Get Jinja2 Template by Template Name (Plain Text)
@router.get("/templates/{template_name}/jinja2", response_class=PlainTextResponse, name="read_jinja2_template",
            dependencies=[Depends(check_permission)])
async def read_jinja2_template(template_name: str, db = Depends(get_database)):
    """Read the jinja2_template of a config template by its name, returning it as plain text."""
    logger.info(f"Entering /templates/{template_name}/jinja2 (GET) endpoint")
    template = await db["config_templates"].find_one({"template_name": template_name})
    if template is None:
        raise HTTPException(status_code=404, detail="Template not found")

    jinja2_template = template.get("jinja2_template")  # Get the jinja2_template value
    if jinja2_template is None:
        raise HTTPException(status_code=404, detail="Jinja2 template not found for this template")

    return PlainTextResponse(jinja2_template, media_type="text/plain")