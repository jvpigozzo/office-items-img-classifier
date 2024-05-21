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


@router.put("/labels/{label_id}", tags=["labels"])
async def update_label(label_id: str, label: LabelUpdate):
    label = dict(label)
    result = db.labels.update_one({"_id": int(label_id)}, {"$set": label})
    if result.matched_count == 0:
        raise HTTPException(
            status_code=404, detail=f"Label with ID {label_id} not found"
        )
    return {"message": "Label updated"}


@router.delete("/labels/{label_id}", tags=["labels"])
async def delete_label(label_id: str):
    result = db.labels.delete_one({"_id": int(label_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404, detail=f"Label with ID {label_id} not found"
        )
    return {"message": "Label deleted"}
