from bson import ObjectId
from database import get_database
from schemas.item import serialize_dict

db = get_database()


async def get_by_id(id):
    return serialize_dict(db.items.find_one({"_id": ObjectId(id)}))


async def push_img_url(id, image_url: str) -> bool:
    db.items.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": {"image_url": image_url}}
    )
    return True
