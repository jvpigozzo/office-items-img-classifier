import os
from random import randint
from bson import ObjectId
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from database import get_database
from utils import save_img, rise_http_exception, get_response
from services import item as service
from schemas.item import ItemCreate, serialize_items, serialize_item


router = APIRouter()
db = get_database()

MEDIA_DIRECTORY = "/vol/media/"


@router.get("/items/", tags=["items"])
async def read_items():
    items = list(db.items.find())
    return serialize_items(items)


@router.get("/items/" + "{id}", tags=["items"])
async def read_item_by_id(id):
    return await check_item(id)


@router.post("/items/", tags=["items"])
async def create_item(item: ItemCreate):
    item_id = db.items.insert_one(item.dict()).inserted_id
    item = db.items.find_one({"_id": item_id})
    return serialize_item(item)


@router.post("/items/image-upload/" + "{id}", tags=["items"])
async def upload_item_img(id: str, image: UploadFile):
    image_name = image.filename
    image_url = save_img(file=image, file_name=image_name)
    done = await service.push_img_url(id, image_url)
    return get_response(
        done,
        success_message="Image saved.",
        error_message="An error occurred while saving user image.",
    )


@router.get("/items/image-show/" + "{id}", tags=["items"])
async def show_item_img(id):
    item = await check_item(id)
    img_url = item["image_url"]
    return FileResponse(img_url)


async def check_item(id: ObjectId) -> dict:
    item = await service.get_by_id(id)
    await rise_http_exception(item, message="Could not find item with the given Id.")
    return item