-- Clean up old products to only show your new ones
-- Run this in MySQL to remove/deactivate old sample products

USE AmafonDB;

-- OPTION 1: See all current products
SELECT product_id, seller_id, name, is_active, created_at 
FROM Products 
ORDER BY created_at DESC;

-- OPTION 2: Deactivate all old hardcoded products (soft delete)
-- This keeps them in database for order history but hides them from view
UPDATE Products 
SET is_active = FALSE 
WHERE name IN ('Blue Eyes White Dragon', 'Super Mario Bros (1985)', 'Veinlite LEDX Vein Finder');

-- OPTION 3: Deactivate ALL products except those created today
-- Uncomment to use:
/*
UPDATE Products 
SET is_active = FALSE 
WHERE DATE(created_at) < CURDATE();
*/

-- OPTION 4: Delete old products that have NO orders (hard delete)
-- This permanently removes products that haven't been ordered
-- Uncomment to use:
/*
DELETE FROM Products 
WHERE product_id NOT IN (SELECT DISTINCT product_id FROM OrderItems)
  AND name IN ('Blue Eyes White Dragon', 'Super Mario Bros (1985)', 'Veinlite LEDX Vein Finder');
*/

-- OPTION 5: Keep ONLY products with 'pencil' in the name
-- Deactivate everything else
-- Uncomment to use:
/*
UPDATE Products 
SET is_active = FALSE 
WHERE LOWER(name) NOT LIKE '%pencil%';

UPDATE Products 
SET is_active = TRUE 
WHERE LOWER(name) LIKE '%pencil%';
*/

-- Verify the changes
SELECT product_id, seller_id, name, is_active, 
       (SELECT COUNT(*) FROM OrderItems WHERE product_id = Products.product_id) as times_ordered
FROM Products 
ORDER BY created_at DESC;
