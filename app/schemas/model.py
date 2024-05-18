from pydantic import BaseModel


class ModelSchema(BaseModel):
    name: str


class ModelCreate(ModelSchema):
    pass


class ModelUpdate(ModelSchema):
    pass


class ModelInDB(ModelSchema):
    id: str


def serialize_model(item):
    item["id"] = str(item["_id"])
    item.pop("_id")
    return item


def serialize_models(items):
    return [serialize_model(item) for item in items]
