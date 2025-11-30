from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class Role(str, Enum):
    customer = "customer"
    seller = "seller"

class Users(BaseModel):
    name: str | None
    email: str
    password: str
    role: Role = Role.customer
    created_at: datetime

# user_id auto-increments in the SQL table, so it is separate from users
class UsersRead(Users):
    user_id: int | None