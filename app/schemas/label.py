from pydantic import BaseModel


class LabelSchema(BaseModel):
    name: str


class LabelCreate(LabelSchema):
    pass


class LabelUpdate(LabelSchema):
    pass


class LabelInDB(LabelSchema):
    id: str


def serialize_label(item):
    item["id"] = str(item["_id"])
    item.pop("_id")
    return item


def serialize_labels(items):
    return [serialize_label(item) for item in items]
