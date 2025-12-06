# Amafon
E-Commerce Site with MySQL integration
The version used in the video demo is located in the branch, demo. (not merged to main currently)

## Overview
Amafon is a full-stack e-commerce platform with a FastAPI backend and vanilla JavaScript frontend. It includes complete CRUD operations for products, orders, users, sellers, and more.

## Features
- ✅ Product management (Create, Read, Update, Delete)
- ✅ Shopping cart functionality with localStorage
- ✅ Order creation and tracking
- ✅ Seller profile management
- ✅ Dynamic user/seller system
- ✅ Image upload support
- ✅ Database integration with MySQL

## Recent Updates

### Database Integration
- All product operations now properly save to and retrieve from MySQL database
- Products created or edited appear immediately on homepage and seller profile
- Orders are saved to database with proper order items tracking
- Delete operations work correctly across all entities

### User Management
- Implemented dynamic user/seller ID system using localStorage
- Default user initialization (User ID: 1, Seller ID: 1)
- Visit `init-user.html` to set custom user IDs
- Current user displayed in homepage header

### Product Features
- Create new products via `createlisting.html`
- Edit product attributes in seller profile modal
- Products automatically refresh on all pages after create/edit/delete
- Only product owners see delete button on homepage
- Full attribute editing: name, description, price, stock, category, image URL

### Order Management
- Orders created from checkout save to database
- Order status updates persist in database
- Delete orders from database via orders page
- View order history with items and totals

## Setup Instructions

### Backend Setup
1. Install Python dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Configure database in `backend/database.py`:
   ```python
   DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/amafondb"
   ```

3. Import the database schema:
   ```bash
   mysql -u username -p amafondb < backend/amafon.sql
   ```

4. Run the server:
   ```bash
   python run_server.py
   ```
   Server will run on `http://127.0.0.1:8007`

### Frontend Setup
1. Open any HTML file in `frontend/` directory with a browser
2. Recommended starting point: `index.html`
3. Optional: Set custom user IDs via `init-user.html`

## API Endpoints

### Products
- `GET /api/products/` - List all products
- `GET /api/products/id/{product_id}` - Get specific product
- `POST /api/products/` - Create new product
- `PUT /api/products/{product_id}` - Update product (supports partial updates)
- `DELETE /api/products/{product_id}` - Delete product

### Orders
- `GET /api/orders/all/list` - List all orders
- `GET /api/orders/all/list-with-items` - List orders with item details
- `POST /api/orders/create-from-cart` - Create order from cart
- `PUT /api/orders/{order_id}/status` - Update order status
- `DELETE /api/orders/delete/{order_id}` - Delete order

### Other Endpoints
- `POST /upload-image` - Upload product images
- See route files in `backend/routes/` for complete API documentation

## File Structure
```
Amafon/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # Database configuration
│   ├── routes/              # API route handlers
│   ├── crud/                # Database operations
│   └── schemas/             # Pydantic models
├── frontend/
│   ├── index.html           # Homepage with product grid
│   ├── seller-profile.html  # Seller dashboard with edit modal
│   ├── createlisting.html   # Create new product
│   ├── checkout.html        # Shopping cart checkout
│   ├── orders.html          # Order history
│   └── init-user.html       # Set current user/seller
└── uploads/                 # Product images

```

## Usage Guide

### Creating a Product
1. Navigate to "Create Listing" page
2. Fill in product details
3. Upload an image (JPG recommended)
4. Click "Create Listing"
5. Product appears in seller profile and homepage immediately

### Editing a Product
1. Go to "Seller Profile" page
2. Find your product
3. Click "Edit" button
4. Modify any attributes in the modal
5. Click "Save Changes"
6. Changes reflect immediately across all pages

### Managing Orders
1. Add products to cart on homepage
2. Click "Checkout" button
3. Fill in shipping and payment info
4. Click "Finalize My Order"
5. Order saves to database and appears in "Orders" page
6. Update order status via dropdown
7. Delete orders as needed

### Switching Users
1. Visit `init-user.html`
2. Enter desired User ID and Seller ID
3. Click "Set User"
4. Navigate to homepage
5. User info displays in header

## Technologies Used
- **Backend**: FastAPI, Python 3.10+
- **Database**: MySQL with aiomysql
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **API**: RESTful design
- **Storage**: localStorage for cart/user state

## Notes
- Image uploads save to `uploads/` directory
- Cart persists in localStorage between sessions
- Default user is User ID: 1, Seller ID: 1
- All database operations use async/await
- CORS enabled for local development
