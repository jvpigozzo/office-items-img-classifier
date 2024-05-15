from pydantic import BaseModel, Field, validator


class Label(BaseModel):
    label_id: str = Field(description="Label ID")

    @validator("label_id")
    def validate_label_id(cls, value):
        if value.isdigit():
            raise ValueError("Label id must be an integer")
        return value
