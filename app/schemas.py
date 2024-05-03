from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    email: str
    nickname: str


class UserCreate(UserSchema):
    pass


class UserUpdate(UserSchema):
    pass


class UserInDB(UserSchema):
    id: str


def serialize_user(user):
    user["id"] = str(user["_id"])
    user.pop("_id")
    return user


def serialize_users(users):
    return [serialize_user(user) for user in users]
