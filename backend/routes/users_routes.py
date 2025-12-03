from database import database
from fastapi import APIRouter, HTTPException
from schemas.users import Users
from crud.users_crud import (get_users, get_user, create_user, update_user, delete_user, login_user)

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/", response_model=list[Users])
async def api_get_users(skip: int = 0, limit: int = 10):
    async with database:
        rows = await get_users(skip=skip, limit=limit)
        return [Users(**dict(r)) for r in rows]

@router.get("/{user_id}", response_model=Users)
async def api_get_user(user_id: int):
    async with database:
        d = await get_user(user_id)
        if not d:
            raise HTTPException(404, "Department not found")
        return Users(**d)

@router.post("/", response_model=Users)
async def api_create_user(user: Users):
    async with database:
        try:
            user_id = await create_user(user.name, user.email, user.backupEmail, user.password_hash, user.role)
            row = await database.fetch_one(
                "SELECT * FROM Users WHERE user_id = :id",
                {"id": user_id}
            )
            return Users(**row)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.put("/", response_model=Users)
async def api_update_user(user: Users):
    async with database:
        try:
            await update_user(user.name, user.email, user.backupEmail, user.password_hash, user.role, user.user_id)
            return Users(**user.dict())
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.delete("/{user_id}")
async def api_delete_user(user_id: int):
    async with database:
        deleted = await delete_user(user_id)
        if deleted == 0:
            raise HTTPException(404, "User not found")
        return {"detail": "User deleted"}

@router.post("/{email}/{password}")
async def api_login_user(email: str, password: str):
    async with database:
        user = await login_user(email, password)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        return Users(**user)