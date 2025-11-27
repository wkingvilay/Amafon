-- drop database amafon;

create database amafon;
use amafon;

-- 1. DDL operations
create table users (
    user_id int primary key auto_increment,
    name varchar(100),
    email varchar(100) unique not null,
    password varchar(255),
    role enum('customer','seller') default 'customer',
    created_at timestamp default current_timestamp
);
create index user_idx on users(user_id);

create table sellers (
    seller_id int primary key auto_increment,
    user_id int,
    brand_name varchar(100),
    constraint sellers_user_fk
		foreign key (user_id) references users(user_id)
		on delete set null
        on update cascade
);
create index seller_idx on sellers(seller_id);

create table categories (
    category_id int primary key auto_increment,
    category_name varchar(100)
);
create index category_idx on categories(category_id);

create table products (
    product_id int primary key auto_increment,
    seller_id int,
    category_id int,
    name varchar(150),
    description text,
    price decimal(10,2),
    stock int check (stock >= 0),
    constraint product_seller_fk
		foreign key (seller_id) references sellers(seller_id)
		on delete set null
        on update cascade,
	constraint product_category_fk
		foreign key (category_id) references categories(category_id)
		on delete set null
        on update cascade
);
create index product_idx on products(product_id);

create table orders (
    order_id int primary key auto_increment,
    user_id int,
    order_date timestamp default current_timestamp,
    total_amount decimal(10,2),
    status enum('pending','shipped','delivered','cancelled'),
    constraint orders_user_fk
		foreign key (user_id) references users(user_id)
		on delete set null
        on update cascade
);
create index order_idx on orders(order_id);

create table orderitems (
    order_item_id int primary key auto_increment,
    order_id int,
    product_id int,
    quantity int check (quantity > 0),
    price decimal(10,2),
    constraint orderitems_order_fk
		foreign key (order_id) references orders(order_id)
        on delete cascade
        on update cascade,
	constraint orderitems_product_fk
    foreign key (product_id) references products(product_id)
		on delete set null
        on update cascade
);
create index orderitem_idx on orderitems(order_item_id);

create table payments (
    payment_id int primary key auto_increment,
    order_id int,
    amount decimal(10,2),
    payment_date timestamp default current_timestamp,
    method enum('credit_card','paypal','gift_card'),
    constraint payments_order_fk
		foreign key (order_id) references orders(order_id)
        on delete set null
        on update cascade
);
create index payment_idx on payments(payment_id);

create table reviews (
    review_id int primary key auto_increment,
    product_id int,
    user_id int,
    rating int check (rating between 1 and 5),
    comment text,
    review_date timestamp default current_timestamp,
    constraint reviews_product_fk
		foreign key (product_id) references products(product_id)
        on delete cascade
        on update cascade,
	constraint reviews_user_fk
		foreign key (user_id) references users(user_id)
        on delete set null
        on update cascade
);
create index review_idx on reviews(review_id);

-- 2. DML Operations 
insert into users (name, email, role) values
	('Rick Harrison', 'harryr@mypawnshop.com', 'seller'),
	('Big Bogus', 'buymymixtape@deathrowrecords.com', 'customer'),
	('Vlad Dracul', 'zzzzzszz@uri.edu', 'customer'),
	('Ryan Tsang', 'ohheythatsme@uri.edu', 'customer'),
	('Vine Swinger', 'vinefromvineswinger123@uri.edu', 'customer');
select * from users;

insert into sellers (user_id, brand_name) values
	(1, 'rick harrison\'s pawn shop');
select * from sellers;

insert into categories (category_name) values
	('electronics'), ('books'), ('clothing'), ('toys & games'), ('video games & consoles'), ('industrial & scientific');
select * from categories;

insert into products (seller_id, category_id, name, description, price, stock) values
	(1, 1, 'blue eyes white dragon', 'yu-gi-oh card', 1000000, 1),
	(1, 1, 'super mario brothers (1985)', 'sealed, authentic, copy of the original super mario bros. for the nintendo entertainment system', 100000.00, 1),
	(1, 1, 'veinlite ledx vein finder', 'veinlite ledx is the leading vein access device in the field of sclerotherapy. 
	ledx was designed with the largest vein imaging area, 
	allowing for fast and efficient treatment sessions.', 679.00, 1),
    (1, 4, 'literal potato head', 'fruits of the earth (not really)', 1.00, 20);
select * from products;

insert into orders (user_id, status) values
 	(2, 'pending'),
    (4, 'cancelled');
select * from orders;

insert into orderitems (order_id, product_id, quantity, price) values
	(1, 1, 1, 1000000.00),
	(1, 2, 1, 100000.00),
	(1, 3, 1, 679.00),
    (2, 4, 19, 1.00),
    (2, 2, 2, 100000.00);
select * from orderitems;

insert into payments (order_id, amount, method) values
	(1, 1100000.00, 'credit_card');
select * from payments;

insert into reviews (product_id, user_id, rating, comment) values
	(1, 1, 1, 'lol'),
	(2, 1, 1, 'fake, the seller is a fraud'),
	(3, 1, 5, 'great product, my patients love it');
select * from reviews;

-- alter table
alter table users add phone_number varchar(15);
-- update
update users set phone_number = '401-555-1234' where user_id = 2;
-- delete
delete from users where user_id = 3;

select * from users;
select * from sellers;

-- 3. Special queries and objects

-- this query shows each user and the products they’ve ordered. 
-- the outer join ensures that even customers who haven’t placed any orders yet still appear in the results.
select u.name as customer_name, o.order_id, p.name as product_name
from users u
left join orders o on u.user_id = o.user_id
left join orderitems oi on o.order_id = oi.order_id
left join products p on oi.product_id = p.product_id;

-- this nested query compares each product’s price to the overall average price, 
-- showing only the more expensive items.
select name, price
from products
where price > (
    select avg(price) from products
);

-- this query calculates the total cost of all products in an order and the person who ordered
select u.name, oi.order_id, sum(p.price*oi.quantity) as total from 
	orderitems oi join products p on oi.product_id=p.product_id join orders o on oi.order_id=o.order_id
    join users u on o.user_id= u.user_id
    where oi.order_id = 2;

-- this is an example of a check placed on products such that the stock
-- of an product cannot fall below 0 in the database
update products set stock=0 where product_id = 1;
-- update products set stock=-1 where product_id = 1;
select * from products;

-- this creates a reusable virtual table that always shows our top-rated products
-- those with an average rating of 4.5 or higher. i can query it later just like a normal table
create view topratedproducts as
select p.name, s.brand_name, avg(r.rating) as avg_rating
from products p
join sellers s on p.seller_id = s.seller_id
join reviews r on p.product_id = r.product_id
group by p.name, s.brand_name
having avg_rating >= 4.5;
select * from topratedproducts;
