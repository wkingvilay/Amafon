from database import database
from fastapi import APIRouter, HTTPException, Query
from schemas.products import Products, ProductsRead
from crud.products_crud import get_products, get_product, create_product, update_product, delete_product, search_product

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/", response_model=list[ProductsRead])
async def api_get_products(skip: int = 0, limit: int = 10):
    async with database:
        rows = await get_products(skip=skip, limit=limit)
        return [ProductsRead(**dict(r)) for r in rows]

@router.get("/id/{product_id}", response_model=ProductsRead)
async def api_get_product(product_id: int):
    async with database:
        d = await get_product(product_id)
        if not d:
            raise HTTPException(status_code=404, detail="Product not found")
        return ProductsRead(**dict(d))

@router.post("/", response_model=ProductsRead)
async def api_create_product(product: Products):
    async with database:
        try:
            product_id = await create_product(product.seller_id, product.category_id, product.name,
                                              product.description, product.price, product.stock)
            return ProductsRead(product_id=product_id, **dict(product))
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.put("/", response_model=ProductsRead)
async def api_update_product(product: ProductsRead):
    async with database:
        try:
            await update_product(product.category_id, product.name, product.description,
                                 product.price, product.stock, product.product_id)
            return ProductsRead(**dict(product))
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.delete("/{product_id}")
async def api_delete_product(product_id: int):
    async with database:
        deleted = await delete_product(product_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"detail": "Product deleted"}

# Note, this isn't the only "get" url, so it must be differentiated somehow
@router.get("/search", response_model=list[ProductsRead])
async def api_search_product(key: str = Query(..., min_length=1)):
    async with database:
        rows = await search_product(key)
        return [ProductsRead(**dict(r)) for r in rows]