from ..database import database
from fastapi import APIRouter, HTTPException, Query
from ..schemas.products import Products
from ..crud.products_crud import get_products, get_product, create_product, update_product, delete_product, search_product

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/", response_model=list[Products])
async def api_get_products(skip: int = 0, limit: int = 10):
    async with database:
        rows = await get_products(skip=skip, limit=limit)
        return [Products(**dict(r)) for r in rows]

@router.get("/id/{product_id}", response_model=Products)
async def api_get_product(product_id: int):
    async with database:
        d = await get_product(product_id)
        if not d:
            raise HTTPException(status_code=404, detail="Product not found")
        return Products(**dict(d))

# @router.post("/", response_model=Products)
# async def api_create_product(product: Products):
#     async with database:
#         try:
#             product_id = await create_product(product.seller_id, product.category_id, product.name,
#                                               product.description, product.price, product.stock, product.image_url)
#             row = await database.fetch_one(
#                 "SELECT * FROM Products WHERE product_id = :id",
#                 {"id": product_id}
#             )
#             return Products(**row)
#         except ValueError as err:
#             raise HTTPException(status_code=400, detail=str(err))

@router.post("/", response_model=Products)
async def api_create_product(product_data: dict):
    async with database:
        try:
            # Get data from request
            seller_id = product_data.get("seller_id", 1)
            category_id = product_data.get("category_id", 1)
            name = product_data.get("name", "Unnamed Product")
            description = product_data.get("description", "")
            price = float(product_data.get("price", 0))
            stock = int(product_data.get("stock", 0))
            image_url = product_data.get("image_url", "https://via.placeholder.com/150")

            # Insert product
            product_id = await create_product(
                seller_id,
                category_id,
                name,
                description,
                price,
                stock,
                image_url
            )

            # Fetch the created product
            row = await database.fetch_one(
                "SELECT * FROM Products WHERE product_id = :id",
                {"id": product_id}
            )

            if row:
                return Products(**dict(row))
            else:
                return Products(
                    product_id=product_id,
                    seller_id=seller_id,
                    category_id=category_id,
                    name=name,
                    description=description,
                    price=price,
                    stock=stock,
                    image_url=image_url,
                    is_active=True
                )

        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.put("/", response_model=Products)
async def api_update_product(product: Products):
    async with database:
        try:
            await update_product(
                product.category_id, 
                product.name, 
                product.description,
                product.price, 
                product.stock, 
                product.image_url, 
                product.is_active,
                product.product_id
            )
            return Products(**dict(product))
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
@router.get("/search", response_model=list[Products])
async def api_search_product(key: str = Query(..., min_length=1)):
    async with database:
        rows = await search_product(key)
        return [Products(**dict(r)) for r in rows]