from bson import ObjectId
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from database import get_database
from utils import save_img, rise_http_exception, get_response, encode_image
from services import item as service
from schemas.item import ItemCreate, serialize_items, serialize_item
from schemas.label import serialize_labels
from classifier import model_pipeline
from models import Label
from prompts import PromptGenerator

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


@router.post("/items/recognize/" + "{id}", tags=["items"])
async def get_item_recognition(
    id: str,
    prompt_template: str,
):
    item = await check_item(id)
    img_path = item["image_url"]
    with open(img_path, mode="rb") as file:
        content = file.read()
    image_str = encode_image(content)
    labels = serialize_labels(list(db.labels.find()))
    labels = {item["id"]: item["name"] for item in labels}
    prompt = PromptGenerator(
        model_class=Label, template=prompt_template, labels=labels
    ).prompt.text
    classifier = model_pipeline(prompt=prompt, image_str=image_str)
    return classifier


async def check_item(id: ObjectId) -> dict:
    item = await service.get_by_id(id)
    await rise_http_exception(item, message="Could not find item with the given Id.")
    return item
