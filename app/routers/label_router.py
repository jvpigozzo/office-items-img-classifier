from fastapi import APIRouter, HTTPException
from schemas.label import (
    LabelCreate,
    LabelInDB,
    LabelUpdate,
    serialize_labels,
    serialize_label,
)
from database import get_database
from bson import ObjectId

router = APIRouter()

db = get_database()

# Counter collection
counter_collection = db["counters"]


@router.get("/labels/", tags=["labels"])
async def read_labels():
    labels = list(db.labels.find())
    return serialize_labels(labels)


@router.post("/labels/", response_model=LabelInDB, tags=["labels"])
async def create_label(label: LabelCreate):
    counter = counter_collection.find_one_and_update(
        {"_id": "label_id"}, {"$inc": {"seq": 1}}, return_document=True, upsert=True
    )
    label_id = counter["seq"]
    label_id = db.labels.insert_one({**label.dict(), "_id": label_id}).inserted_id
    label = db.labels.find_one({"_id": label_id})
    return serialize_label(label)
