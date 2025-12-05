from ..database import database
from fastapi import APIRouter, HTTPException
from ..schemas.categories import Categories
from ..crud.categories_crud import get_categories, get_category, create_category, update_category, delete_category

router = APIRouter(prefix="/api/categories", tags=["Categories"])

@router.get("/", response_model=list[Categories])
async def api_get_categories():
    async with database:
        rows = await get_categories()
        return [Categories(**dict(r)) for r in rows]

@router.get("/{category_id}", response_model=Categories)
async def api_get_category(category_id: int):
    async with database:
        d = await get_category(category_id)
        if not d:
            raise HTTPException(status_code=404, detail="Category not found")
        return Categories(**d)

@router.post("/", response_model=Categories)
async def api_create_category(category: Categories):
    async with database:
        try:
            category_id = await create_category(category.category_name)
            row = await database.fetch_one(
                "SELECT * FROM Categories WHERE category_id = :id",
                {"id": category_id}
            )
            return Categories(**row)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.put("/", response_model=Categories)
async def api_update_category(category: Categories):
    async with database:
        try:
            await update_category(category.category_name, category.category_id)
            return Categories(**dict(category))
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.delete("/{category_name}")
async def api_delete_category(category_name: str):
    async with database:
        deleted = await delete_category(category_name)
        if deleted == 0:
            raise HTTPException(status_code=404, detail="Category not found")
        return {"detail": f"Category {category_name} deleted"}