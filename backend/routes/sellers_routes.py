from database import database
from fastapi import APIRouter, HTTPException
from schemas.sellers import Sellers, Sellers
from crud.sellers_crud import get_seller, create_seller, update_seller, delete_seller

router = APIRouter(prefix="/api/Sellers", tags=["Sellers"])

@router.get("/{seller_id}", response_model=Sellers)
async def api_get_seller(seller_id: int):
    async with database:
        d = await get_seller(seller_id)
        if not d:
            raise HTTPException(status_code=404, detail="Seller not found")
        return Sellers(**d)

@router.post("/", response_model=Sellers)
async def api_create_user(seller: Sellers):
    async with database:
        try:
            seller_id = await create_seller(seller.user_id, seller.store_name, seller.rating)
            row = await database.fetch_one(
                "SELECT * FROM Sellers WHERE seller_id = :id",
                {"id": seller_id}
            )
            return Sellers(**row)
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.put("/", response_model=Sellers)
async def api_update_user(seller: Sellers):
    async with database:
        try:
            await update_seller(seller.store_name, seller.seller_id, seller.rating)
            return Sellers(**seller.dict())
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.delete("/{seller_id}")
async def api_delete_seller(seller_id: int):
    async with database:
        deleted = await delete_seller(seller_id)
        if not deleted:
            raise HTTPException(404, "Seller not found")
        return {"detail": "Seller deleted"}