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

# Mount frontend directory as static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        if not file or not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Read file content first
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Validate file type by content-type
        allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
        if file.content_type and file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail=f"Invalid file type. Received: {file.content_type}. Only images allowed (JPEG, PNG, GIF, WebP).")
        
        # Create unique filename to avoid conflicts
        import uuid
        file_ext = file.filename.split('.')[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        file_location = f"{UPLOAD_DIR}/{unique_filename}"
        
        # Ensure uploads directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        with open(file_location, "wb") as f:
            f.write(contents)
        
        # Return HTTP URL instead of file path
        file_url = f"http://127.0.0.1:8007/uploads/{unique_filename}"
        return {"file_url": file_url}
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Upload error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8007, reload=True)