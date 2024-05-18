from bson import ObjectId
from fastapi.responses import FileResponse
from fastapi import APIRouter, File, UploadFile, HTTPException

from schemas.item import ItemCreate, ItemUpdate, serialize_items, serialize_item

from database import get_database
from classifier import ModelPipeline
from services import item as service
from utils import save_img, rise_http_exception, get_response

router = APIRouter()
db = get_database()


@router.get("/items/", tags=["items"])
async def read_items():
    items = list(db.items.find())
    return serialize_items(items)


@router.get("/items/" + "{id}", tags=["items"])
async def read_item_by_id(id):
    return await check_item(id)


@router.post("/items/", tags=["items"])
async def create_item(item: ItemCreate):
    label_id = int(item.label_id)
    label_exists = db.labels.find_one({"_id": label_id})
    if not label_exists:
        return {"error": "Label with the given ID does not exist."}, 404
    item_id = db.items.insert_one(item.dict()).inserted_id
    item = db.items.find_one({"_id": item_id})
    return serialize_item(item)


@router.put("/items/{item_id}", tags=["items"])
async def update_item(item_id: str, item: ItemUpdate):
    update_data = {k: v for k, v in item.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    result = db.items.update_one({"_id": ObjectId(item_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    return {"message": "Item updated"}


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


@router.post("/items/recognize/" + "{item_id}", tags=["items"])
async def get_item_recognition(item_id: str, prompt_template: str, model_name: str):
    item = await check_item(item_id)
    img_path = item["image_url"]
    classifier = ModelPipeline(
        prompt_template=prompt_template, img_path=img_path, model_name=model_name
    )
    img_class = classifier.process()
    result = db.items.update_one({"_id": ObjectId(item_id)}, {"$set": img_class})
    if result.matched_count == 0:
        raise HTTPException(
            status_code=404, detail=f"Could not update item with ID {item_id}"
        )
    return img_class


async def check_item(id: ObjectId) -> dict:
    item = await service.get_by_id(id)
    await rise_http_exception(item, message="Could not find item with the given Id.")
    return item
