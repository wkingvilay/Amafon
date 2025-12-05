import uvicorn
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware

from .database import database, DATABASE_URL
from starlette_admin.contrib.sqla import Admin
from sqlalchemy.ext.asyncio import create_async_engine

from .routes.users_routes import router as users_router
from .routes.sellers_routes import router as sellers_router
from .routes.categories_routes import router as categories_router
from .routes.products_routes import router as products_router
from .routes.orders_routes import router as orders_router
from .routes.orderitems_routes import router as orderitems_router
from .routes.payments_routes import router as payments_router
from .routes.reviews_routes import router as reviews_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    print("Database connection established")

    # Test: fetch database name
    result = await database.fetch_one("SELECT DATABASE() AS db_name;")
    print("Currently connected to:", result["db_name"])

    yield
    await database.disconnect()
    print("Database disconnection established")

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(sellers_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(orderitems_router)
app.include_router(payments_router)
app.include_router(reviews_router)

# Create SQLAlchemy engine for admin
engine = create_async_engine(DATABASE_URL)

# Create admin instance without SQLAlchemy engine (for custom raw SQL views)
admin = Admin(
    engine=engine,
    title="Database Admin Panel",
    base_url="/admin"
)

admin.mount_to(app)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Amafon",
        "dashboard_url": "/dashboard",
        "admin_url": "/admin",
        "api_docs": "/docs"
    }

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount uploads directory as static files
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Validate file type
        allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type. Only images allowed.")
        
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        
        with open(file_location, "wb") as f:
            contents = await file.read()
            f.write(contents)
        
        # Return HTTP URL instead of file path
        file_url = f"http://127.0.0.1:8007/uploads/{file.filename}"
        return {"file_url": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8007, reload=True)