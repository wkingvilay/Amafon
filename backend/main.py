import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from starlette.middleware.cors import CORSMiddleware

from database import database, DATABASE_URL
from starlette_admin.contrib.sqla import Admin
from sqlalchemy.ext.asyncio import create_async_engine

from routes.users_routes import router as users_router
from routes.sellers_routes import router as sellers_router
from routes.categories_routes import router as categories_router
from routes.products_routes import router as products_router
from routes.orders_routes import router as orders_router
from routes.orderitems_routes import router as orderitems_router
from routes.payments_routes import router as payments_router
from routes.reviews_routes import router as reviews_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    print("Database connection established")
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8007, reload=True)