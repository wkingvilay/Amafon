from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class Role(str, Enum):
    customer = "customer"
    seller = "seller"
    admin = "admin"

class Users(BaseModel):
    user_id: int
    name: str
    email: str
    backupEmail: str | None
    password_hash: str
    role: Role = Role.customer
    created_at: datetime
    updated_at: datetime | None