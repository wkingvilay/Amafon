# Testing Guide - Amafon

## Quick Start Testing

### 1. Start the Backend Server
```powershell
cd c:\Users\juddl\Downloads\Amafon-main\Amafon-main
python run_server.py
```
Expected output: Server running on http://127.0.0.1:8007

### 2. Open Frontend
Open `frontend/index.html` in your browser or use Live Server

### 3. Test Product Creation
1. Navigate to **Create Listing** page
2. Fill in:
   - Product Name: "Test Product"
   - Description: "Test description"
   - Price: 29.99
   - Stock: 10
   - Category: Electronics
   - Upload any image
3. Click **Create Listing**
4. Verify:
   - ✅ Success message appears
   - ✅ Redirects to seller profile
   - ✅ Product appears in seller profile
   - ✅ Navigate to homepage - product appears there too
   - ✅ Check database: `SELECT * FROM Products ORDER BY product_id DESC LIMIT 1;`

### 4. Test Product Editing
1. Go to **Seller Profile** page
2. Find your product
3. Click **Edit** button
4. Change:
   - Price: 39.99
   - Stock: 5
5. Click **Save Changes**
6. Verify:
   - ✅ Success message appears
   - ✅ Product card updates immediately
   - ✅ Navigate to homepage - changes reflected
   - ✅ Check database: `SELECT price, stock FROM Products WHERE product_id = X;`

### 5. Test Product Deletion
1. On **Homepage**, find a product you own
2. Click **Delete** button (🗑️)
3. Confirm deletion
4. Verify:
   - ✅ Success message appears
   - ✅ Product disappears from homepage
   - ✅ Product removed from seller profile
   - ✅ Check database: Product no longer exists

### 6. Test Shopping Cart & Orders
1. On **Homepage**, click **Add to Cart** on several products
2. Verify cart updates in the right sidebar
3. Click **Checkout** button
4. Fill in shipping information:
   - Full Name: "John Doe"
   - Address: "123 Test St"
   - City: "Test City"
   - ZIP: "12345"
5. Fill in payment info (any values for testing)
6. Click **Finalize My Order**
7. Verify:
   - ✅ Success modal appears
   - ✅ Redirects to orders page
   - ✅ Order appears in orders list
   - ✅ Check database: `SELECT * FROM Orders ORDER BY order_id DESC LIMIT 1;`
   - ✅ Check order items: `SELECT * FROM OrderItems WHERE order_id = X;`

### 7. Test Order Management
1. On **Orders** page
2. Change order status using dropdown (Pending → Shipped → Delivered)
3. Verify:
   - ✅ Status updates in UI
   - ✅ Success alert appears
   - ✅ Check database: `SELECT status FROM Orders WHERE order_id = X;`
4. Click **Delete** button on an order
5. Verify:
   - ✅ Confirmation dialog appears
   - ✅ Order disappears from list
   - ✅ Check database: Order deleted

### 8. Test Multi-Seller Scenario
1. Open **init-user.html**
2. Set User ID: 2, Seller ID: 2
3. Click **Set User**
4. Go to **Homepage**
5. Verify: User info shows "User #2 | Seller #2"
6. Go to **Create Listing** and create a product
7. Verify:
   - ✅ Product created with seller_id = 2
   - ✅ Check database: `SELECT seller_id FROM Products WHERE product_id = X;`
8. Go back to **Homepage**
9. Verify:
   - ✅ Products from seller 1 don't have delete button
   - ✅ Products from seller 2 have delete button
10. Switch back to User 1 via init-user.html
11. Verify correct products show delete buttons

## Database Verification Queries

### Check recent products
```sql
SELECT product_id, seller_id, name, price, stock, created_at 
FROM Products 
ORDER BY created_at DESC 
LIMIT 10;
```

### Check recent orders
```sql
SELECT o.order_id, o.user_id, o.status, o.total_amount, o.order_date,
       COUNT(oi.order_item_id) as item_count
FROM Orders o
LEFT JOIN OrderItems oi ON o.order_id = oi.order_id
GROUP BY o.order_id
ORDER BY o.order_date DESC
LIMIT 10;
```

### Check order details
```sql
SELECT oi.*, p.name as product_name
FROM OrderItems oi
JOIN Products p ON oi.product_id = p.product_id
WHERE oi.order_id = X;
```

### Check seller's products
```sql
SELECT product_id, name, price, stock, is_active
FROM Products
WHERE seller_id = 1
ORDER BY created_at DESC;
```

## Common Issues & Solutions

### Issue: Products not appearing after creation
**Solution**: Check browser console for errors. Verify:
- Backend server is running
- Database connection is working
- No CORS errors

### Issue: Edit modal not opening
**Solution**: 
- Check browser console for JavaScript errors
- Verify product data is loading correctly
- Clear browser cache and reload

### Issue: Orders not saving to database
**Solution**:
- Check that `/api/orders/create-from-cart` endpoint exists
- Verify OrderItems are being created
- Check backend logs for errors

### Issue: Wrong user/seller ID
**Solution**:
- Visit `init-user.html` and set correct IDs
- Check localStorage in browser DevTools
- Refresh the page after setting user

### Issue: Images not displaying
**Solution**:
- Verify uploads directory exists
- Check image URL in database
- Ensure backend is serving `/uploads` static files
- Use placeholder URL if image upload fails

## Expected Behavior Summary

✅ **Product Creation**: Saves to DB → Shows in seller profile → Shows on homepage
✅ **Product Editing**: Updates DB → Refreshes immediately on all pages
✅ **Product Deletion**: Removes from DB → Disappears from all pages
✅ **Order Creation**: Saves order + items to DB → Shows in orders page
✅ **Order Updates**: Status changes persist in DB
✅ **User Management**: Dynamic user/seller IDs from localStorage
✅ **Cart**: Persists in localStorage between sessions
✅ **Navigation**: All links work correctly (index.html, not amafon.html)

## API Testing with curl

### Create a product
```powershell
curl -X POST "http://127.0.0.1:8007/api/products/" -H "Content-Type: application/json" -d '{\"seller_id\": 1, \"category_id\": 1, \"name\": \"API Test Product\", \"description\": \"Created via API\", \"price\": 99.99, \"stock\": 5, \"image_url\": \"https://via.placeholder.com/300\"}'
```

### Update a product
```powershell
curl -X PUT "http://127.0.0.1:8007/api/products/1" -H "Content-Type: application/json" -d '{\"price\": 149.99, \"stock\": 3}'
```

### Delete a product
```powershell
curl -X DELETE "http://127.0.0.1:8007/api/products/1"
```

### Get all products
```powershell
curl "http://127.0.0.1:8007/api/products/"
```

### Create an order
```powershell
curl -X POST "http://127.0.0.1:8007/api/orders/create-from-cart" -H "Content-Type: application/json" -d '{\"user_id\": 1, \"shipping_address\": \"123 API St\", \"items\": [{\"product_id\": 1, \"name\": \"Test\", \"price\": 10, \"quantity\": 2}], \"total\": 25.00}'
```

## Success Criteria

All tests pass when:
1. ✅ Products persist in database after creation
2. ✅ Edits update database and UI simultaneously  
3. ✅ Deletions remove from database and all pages
4. ✅ Orders save with proper items and totals
5. ✅ User switching works correctly
6. ✅ Cart functionality persists
7. ✅ No hardcoded IDs in normal operation
8. ✅ All navigation links work
9. ✅ API endpoints respond correctly
10. ✅ Database constraints are respected
