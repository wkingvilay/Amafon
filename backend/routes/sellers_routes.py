from database import database
from fastapi import APIRouter, HTTPException
from schemas.sellers import Sellers, SellersRead
from crud.sellers_crud import get_seller, create_seller, update_seller, delete_seller

router = APIRouter(prefix="/api/Sellers", tags=["Sellers"])

@router.get("/{seller_id}", response_model=SellersRead)
async def api_get_seller(seller_id: int):
    async with database:
        d = await get_seller(seller_id)
        if not d:
            raise HTTPException(status_code=404, detail="Seller not found")
        return SellersRead(**d)

@router.post("/", response_model=SellersRead)
async def api_create_user(seller: Sellers):
    async with database:
        try:
            seller_id = await create_seller(seller.user_id, seller.brand_name)
            return SellersRead(seller_id=seller_id, **seller.dict())
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.put("/", response_model=SellersRead)
async def api_update_user(seller: SellersRead):
    async with database:
        try:
            await update_seller(seller.brand_name, seller.seller_id)
            return SellersRead(**seller.dict())
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.delete("/{seller_id}")
async def api_delete_seller(seller_id: int):
    async with database:
        deleted = await delete_seller(seller_id)
        if not deleted:
            raise HTTPException(404, "Seller not found")
        return {"detail": "Seller deleted"}