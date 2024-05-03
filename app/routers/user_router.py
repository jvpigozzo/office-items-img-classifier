from fastapi import APIRouter, HTTPException
from schemas import UserCreate, UserInDB, UserUpdate, serialize_users, serialize_user
from database import get_database
from bson import ObjectId


router = APIRouter()

db = get_database()


@router.get("/users/")
async def read_users():
    users = list(db.users.find())
    return serialize_users(users)


@router.post("/users/", response_model=UserInDB)
async def create_user(user: UserCreate):
    user_id = db.users.insert_one(user.dict()).inserted_id
    user = db.users.find_one({"_id": user_id})
    return serialize_user(user)


@router.put("/users/{user_id}")
async def update_user(user_id: str, user: UserUpdate):
    user = dict(user)
    result = db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return {"message": "User updated"}


@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    result = db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return {"message": "User deleted"}
