from fastapi import APIRouter, HTTPException
from schemas.model import (
    ModelCreate,
    ModelInDB,
    ModelUpdate,
    serialize_models,
    serialize_model,
)
from database import get_database
from bson import ObjectId

router = APIRouter()

db = get_database()

# Counter collection
counter_collection = db["counters"]


@router.get("/models/", tags=["models"])
async def read_models():
    models = list(db.models.find())
    return serialize_models(models)


@router.post("/models/", response_model=ModelInDB, tags=["models"])
async def create_model(model: ModelCreate):
    counter = counter_collection.find_one_and_update(
        {"_id": "model_id"}, {"$inc": {"seq": 1}}, return_document=True, upsert=True
    )
    model_id = counter["seq"]
    model_id = db.models.insert_one({**model.dict(), "_id": model_id}).inserted_id
    model = db.models.find_one({"_id": model_id})
    return serialize_model(model)


@router.put("/models/{model_id}", tags=["models"])
async def update_model(model_id: str, model: ModelUpdate):
    model = dict(model)
    result = db.models.update_one({"_id": int(model_id)}, {"$set": model})
    if result.matched_count == 0:
        raise HTTPException(
            status_code=404, detail=f"model with ID {model_id} not found"
        )
    return {"message": "model updated"}


@router.delete("/models/{model_id}", tags=["models"])
async def delete_model(model_id: str):
    result = db.models.delete_one({"_id": ObjectId(model_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404, detail=f"model with ID {model_id} not found"
        )
    return {"message": "model deleted"}
