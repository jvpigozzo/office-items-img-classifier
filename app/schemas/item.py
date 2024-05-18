from pydantic import BaseModel
from typing import Optional


class ItemSchema(BaseModel):
    name: str
    label_id: str
    is_validated: bool


class ItemCreate(ItemSchema):
    pass


class ItemUpdate(ItemSchema):
    name: Optional[str] = None
    label_id: Optional[str] = None
    is_validated: Optional[bool] = None


def serialize_item(item):
    item["id"] = str(item["_id"])
    item.pop("_id")
    return item


def serialize_items(items):
    return [serialize_item(item) for item in items]


def serialize_dict(entity) -> dict:
    if entity != None:
        return {
            **{i: str(entity[i]) for i in entity if i == "_id"},
            **{i: entity[i] for i in entity if i != "_id"},
        }
    return None
