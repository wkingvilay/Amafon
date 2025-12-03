DROP DATABASE IF EXISTS AmazonDB;
CREATE DATABASE AmazonDB;
USE AmazonDB;

-----------------------------------------------------
-- USERS TABLE (customers + sellers accounts)
-----------------------------------------------------
CREATE TABLE Users (
    user_id        INT PRIMARY KEY AUTO_INCREMENT,
    name           VARCHAR(100) NOT NULL,
    email          VARCHAR(100) UNIQUE NOT NULL,
    backupEmail    VARCHAR(100),
    password_hash  VARCHAR(255) NOT NULL,
    role           ENUM('customer','seller','admin') DEFAULT 'customer',
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-----------------------------------------------------
-- SELLERS TABLE (linked to Users)
-----------------------------------------------------
CREATE TABLE Sellers (
    seller_id   INT PRIMARY KEY AUTO_INCREMENT,
    user_id     INT NOT NULL,
    store_name  VARCHAR(100) UNIQUE NOT NULL,
    rating      DECIMAL(3,2) DEFAULT 0.00,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) 
        ON DELETE CASCADE
);

-----------------------------------------------------
-- CATEGORIES TABLE
-----------------------------------------------------
CREATE TABLE Categories (
    category_id   INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL UNIQUE
);

-----------------------------------------------------
-- PRODUCTS TABLE
-----------------------------------------------------
CREATE TABLE Products (
    product_id     INT PRIMARY KEY AUTO_INCREMENT,
    seller_id      INT NOT NULL,
    category_id    INT,
    name           VARCHAR(150) NOT NULL,
    description    TEXT,
    price          DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    stock          INT NOT NULL CHECK (stock >= 0),
    image_url      VARCHAR(255),
    is_active      BOOLEAN DEFAULT TRUE,
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES Sellers(seller_id) 
        ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

-----------------------------------------------------
-- ORDERS TABLE
-----------------------------------------------------
CREATE TABLE Orders (
    order_id      INT PRIMARY KEY AUTO_INCREMENT,
    user_id       INT NOT NULL,
    order_date    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount  DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
    status        ENUM('Pending','Paid','Shipped','Delivered','Cancelled') 
                      DEFAULT 'Pending',
    shipping_address VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE CASCADE
);

-----------------------------------------------------
-- ORDER ITEMS TABLE
-----------------------------------------------------
CREATE TABLE OrderItems (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id      INT NOT NULL,
    product_id    INT NOT NULL,
    quantity      INT NOT NULL CHECK (quantity > 0),
    price         DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-----------------------------------------------------
-- PAYMENTS TABLE (mock-safe: only last4 digits)
-----------------------------------------------------
CREATE TABLE Payments (
    payment_id       INT PRIMARY KEY AUTO_INCREMENT,
    order_id         INT NOT NULL,
    amount           DECIMAL(10,2) NOT NULL CHECK (amount >= 0),
    payment_date     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    method           ENUM('Credit Card','PayPal','Gift Card') NOT NULL,

    -- mock card info (safe for assignments)
    card_last4       CHAR(4),
    billing_address  VARCHAR(255),

    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
        ON DELETE CASCADE
);

-----------------------------------------------------
-- REVIEWS TABLE
-----------------------------------------------------
CREATE TABLE Reviews (
    review_id    INT PRIMARY KEY AUTO_INCREMENT,
    product_id   INT NOT NULL,
    user_id      INT NOT NULL,
    rating       INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    title        VARCHAR(100),
    comment      TEXT,
    review_date  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE CASCADE
);

-----------------------------------------------------
-- INDEXES FOR PERFORMANCE
-----------------------------------------------------
CREATE INDEX idx_products_seller ON Products(seller_id);
CREATE INDEX idx_products_category ON Products(category_id);
CREATE INDEX idx_orderitems_order ON OrderItems(order_id);
CREATE INDEX idx_reviews_product ON Reviews(product_id);

-----------------------------------------------------
-- SAMPLE DATA INSERTS
-----------------------------------------------------

-- Users
INSERT INTO Users (name, email, password_hash, role) VALUES
('Rick Harrison', 'harryR@mypawnshop.com', 'hash1', 'seller'),
('Customer A', 'customerA@example.com', 'hash2', 'customer'),
('Customer B', 'customerB@example.com', 'hash3', 'customer'),
('Customer C', 'customerC@example.com', 'hash4', 'customer');

-- Sellers
INSERT INTO Sellers (user_id, store_name, rating) VALUES
(1, 'Rick Harrison Pawn Shop', 4.7);

-- Categories
INSERT INTO Categories (category_name) VALUES
('Electronics'), ('Books'), ('Clothing'), ('Games'), ('Industrial');

-- Products
INSERT INTO Products (seller_id, category_id, name, description, price, stock, image_url) VALUES
(1, 1, 'Blue Eyes White Dragon', 'Ultra rare Yu-Gi-Oh card.', 1000000.00, 1, 'blueeyes.jpg'),
(1, 1, 'Super Mario Bros (1985)', 'Sealed NES copy.', 100000.00, 1, 'smb1985.jpg'),
(1, 5, 'Veinlite LEDX Vein Finder', 'Medical vein imaging device.', 679.00, 5, 'veinlite.jpg');

-- Orders
INSERT INTO Orders (user_id, total_amount, status, shipping_address) VALUES
(2, 1100000.00, 'Pending', '123 Fake Street, NY');

-- Order Items
INSERT INTO OrderItems (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 1000000.00),
(1, 2, 1, 100000.00);

-- Payment
INSERT INTO Payments (order_id, amount, method, card_last4, billing_address) VALUES
(1, 1100000.00, 'Credit Card', '1234', '123 Fake Street, NY');

-- Reviews
INSERT INTO Reviews (product_id, user_id, rating, title, comment) VALUES
(1, 1, 1, 'Bad', 'lol'),
(2, 1, 1, 'Fake', 'Fake, seller is fraud'),
(3, 1, 5, 'Great Tool', 'Patients love it');