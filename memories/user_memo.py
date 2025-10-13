from schemas.user_schema import UserSchema
from db.mongo import get_collection

users = get_collection("users")

def insert_user(user: UserSchema):
    users.insert_one(user.model_dump())

def get_user(email: str):
    return users.find_one({"email": email})

