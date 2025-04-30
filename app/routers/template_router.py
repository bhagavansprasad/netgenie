from fastapi import APIRouter, HTTPException, Depends, Query, Body
from fastapi import UploadFile, File
from typing import List, Optional
import logging
from app.core.database import get_database
from bson import ObjectId
from app.schemas.config_template_schema import ConfigTemplateListResponse, ConfigTemplateResponse
from app.core.auth import check_permission
from pymongo import ReturnDocument
from app.models.config_template_model import ConfigTemplate
from fastapi.responses import PlainTextResponse
from app.schemas.user_schemas import UserResponse
from app.core.security import get_current_user

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


# 7. Create Template from Text
@router.post("/templates/text", response_class=PlainTextResponse, status_code=201, name="create_text_template",
             dependencies=[Depends(check_permission)])
async def create_text_template(
    template_name: str = Query(..., title="Template Name", description="The name for the new template"),
    template_content: str = Body(..., media_type="text/plain", title="Template Content", description="The content of the template"),
    current_user: UserResponse = Depends(get_current_user),
    db = Depends(get_database)
):
    """Create a new template from plain text content."""
    logger.info("Entering /templates/text (POST) endpoint")
    logger.debug(f"Template Name: {template_name}")
    logger.debug(f"Template Content: {template_content}")

    # Check if template name already exists
    if await db["config_templates"].find_one({"template_name": template_name}):
        raise HTTPException(status_code=400, detail="Template name already exists")

    # Create ConfigTemplate object
    config_template = ConfigTemplate(
        template_name=template_name,
        username=current_user.username,  # Use username from authenticated user
        device_name="N/A",  # Not applicable for manually created templates
        input_configuration="N/A",  # Not applicable for manually created templates
        jinja2_template=template_content,
        json_variables={}  # Empty JSON variables for manually created templates
    )

    # Insert data into the database
    config_template_dict = config_template.model_dump()
    await db["config_templates"].insert_one(config_template_dict)
    logger.info(f"Template '{template_name}' saved to database.")

    return PlainTextResponse(template_content, media_type="text/plain")

# 8. Create Template from File Upload
@router.post("/templates/file", response_class=PlainTextResponse, status_code=201, name="create_template_from_file",
             dependencies=[Depends(check_permission)])
async def create_template_from_file(
    template_name: str = Query(..., title="Template Name", description="The name for the new template"),
    file: UploadFile = File(..., title="Template File", description="The file containing the template content"),
    current_user: UserResponse = Depends(get_current_user),
    db = Depends(get_database)
):
    """Create a new template by uploading a file."""
    logger.info("Entering /templates/file (POST) endpoint")
    logger.debug(f"Template Name: {template_name}")
    logger.debug(f"Filename: {file.filename}")

    # Check if template name already exists
    if await db["config_templates"].find_one({"template_name": template_name}):
        raise HTTPException(status_code=400, detail="Template name already exists")

    try:
        contents = await file.read()
        template_content = contents.decode()  # Assuming UTF-8 encoding
        logger.debug(f"Template Content: {template_content}")
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        raise HTTPException(status_code=500, detail=f"Error reading file: {e}")
    finally:
        await file.close()

    # Create ConfigTemplate object
    config_template = ConfigTemplate(
        template_name=template_name,
        username=current_user.username,  # Use username from authenticated user
        device_name="N/A",  # Not applicable for manually created templates
        input_configuration="N/A",  # Not applicable for manually created templates
        jinja2_template=template_content,
        json_variables={}  # Empty JSON variables for manually created templates
    )

    # Insert data into the database
    config_template_dict = config_template.model_dump()
    await db["config_templates"].insert_one(config_template_dict)
    logger.info(f"Template '{template_name}' saved to database.")

    return PlainTextResponse(template_content, media_type="text/plain")