-- Fix for Product Deletion Issue
-- This adds CASCADE to OrderItems foreign key for product_id

USE AmafonDB;

-- OPTION 1: Fix the schema to allow hard deletes (WARNING: This will delete order history!)
-- Uncomment the lines below if you want to enable hard deletes

/*
-- Drop the existing foreign key constraint
ALTER TABLE OrderItems DROP FOREIGN KEY orderitems_ibfk_2;

-- Re-add it WITH cascade delete
ALTER TABLE OrderItems 
ADD CONSTRAINT orderitems_ibfk_2 
FOREIGN KEY (product_id) REFERENCES Products(product_id)
ON DELETE CASCADE;
*/

-- OPTION 2: Keep order history safe (RECOMMENDED)
-- The code now uses soft delete automatically when a product has orders
-- Products are marked is_active = FALSE instead of being deleted
-- This preserves order history for business records

-- To manually soft-delete a product:
-- UPDATE Products SET is_active = FALSE WHERE product_id = X;

-- To see all products including inactive ones:
-- SELECT * FROM Products;

-- To see only active products (what customers see):
-- SELECT * FROM Products WHERE is_active = TRUE;

-- To permanently delete a product with no orders:
-- DELETE FROM Products WHERE product_id = X;

-- To check if a product has orders before deleting:
SELECT p.product_id, p.name, 
       COUNT(oi.order_item_id) as times_ordered,
       p.is_active
FROM Products p
LEFT JOIN OrderItems oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name, p.is_active
ORDER BY p.product_id;
