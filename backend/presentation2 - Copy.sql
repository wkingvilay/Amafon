CREATE DATABASE AmazonDB;
USE AmazonDB;

-- 1. 8 Tables comprising of:
-- 		Users 
-- 		Sellers
-- 		Categories
-- 		Products
-- 		Orders
-- 		OrderItems
-- 		Payments
-- 		Reviews

CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    backupEmail VARCHAR(100) NULL,
    password_hash VARCHAR(255),
    role ENUM('customer','seller') DEFAULT 'customer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Sellers (
    seller_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    store_name VARCHAR(100),
    rating DECIMAL(3,2),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100)
);

CREATE TABLE Products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    seller_id INT,
    category_id INT,
    name VARCHAR(150),
    description TEXT,
    price DECIMAL(10,2),
    stock INT CHECK (stock >= 0),
    FOREIGN KEY (seller_id) REFERENCES Sellers(seller_id),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2),
    status ENUM('Pending','Shipped','Delivered','Cancelled'),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE OrderItems (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    product_id INT,
    quantity INT CHECK (quantity > 0),
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE Payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    amount DECIMAL(10,2),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    method ENUM('Credit Card','PayPal','Gift Card'),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

CREATE TABLE Reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    user_id INT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- 2. Data in table 
INSERT INTO Users (name, email, role) VALUES
('Rick Harrison', 'harryR@mypawnshop.com', 'seller'),
('x', 'BuyMyMixtape@deathrowrecords.com', 'customer'),
('y', 'ZZZZZSZZ@uri.edu', 'customer'),
('z', 'ABABABABABABABAl@uri.edu', 'customer'),
('w', 'vinefromvineswinger123@uri.edu', 'customer');

INSERT INTO Sellers (user_id, store_name, rating) VALUES
(1, 'Rick Harrison\'s Pawn Shop', 4.7);

INSERT INTO Categories (category_name) VALUES
('Electronics'), ('Books'), ('Clothing'), ('Toys & Games'), ('Video Games & Consoles'), ('Industrial & Scientific');

INSERT INTO Products (seller_id, category_id, name, description, price, stock) VALUES
(1, 1, 'Blue Eyes White Dragon', 'Yu-Gi-Oh Card', 1000000, 1),
(1, 1, 'Super Mario Brothers (1985)', 'Sealed, authentic, copy of the original Super Mario Bros. for the Nintendo Entertainment System', 100000.00, 1),
(1, 1, 'Veinlite LEDX Vein Finder', 'Veinlite LEDX is the leading vein access device in the field of sclerotherapy. 
									LEDX was designed with the largest vein imaging area, 
                                    allowing for fast and efficient treatment sessions.', 679.00, 1);

INSERT INTO Orders (user_id, total_amount, status) VALUES
(2, 1100000.00, 'Pending');

INSERT INTO OrderItems (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 1000000.00),
(1, 2, 1, 100000.00),
(1, 3, 1, 679.00);

INSERT INTO Payments (order_id, amount, method) VALUES
(1, 1100000.00, 'Credit Card');

INSERT INTO Reviews (product_id, user_id, rating, comment) VALUES
(1, 1, 1, 'lol'),
(2, 1, 1, 'Fake, the seller is a fraud'),
(3, 1, 5, 'Great product, my patients love it');


-- 3. Special Queries

-- This query shows each user and the products they’ve ordered. 
-- The outer join ensures that even customers who haven’t placed any orders yet still appear in the results.
SELECT u.name AS customer_name, o.order_id, p.name AS product_name
FROM Users u
LEFT JOIN Orders o ON u.user_id = o.user_id
LEFT JOIN OrderItems oi ON o.order_id = oi.order_id
LEFT JOIN Products p ON oi.product_id = p.product_id;

-- This nested query compares each product’s price to the overall average price, 
-- showing only the more expensive items.
SELECT name, price
FROM Products
WHERE price > (
    SELECT AVG(price) FROM Products
);

-- his creates a reusable virtual table that always shows our top-rated products
-- those with an average rating of 4.5 or higher. I can query it later just like a normal table
CREATE VIEW TopRatedProducts AS
SELECT p.name, s.store_name, AVG(r.rating) AS avg_rating
FROM Products p
JOIN Sellers s ON p.seller_id = s.seller_id
JOIN Reviews r ON p.product_id = r.product_id
GROUP BY p.name, s.store_name
HAVING avg_rating >= 4.5;

SELECT * FROM TopRatedProducts;

