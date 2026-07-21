show databases;
use test;
show tables;
select * from amazon_sales;
SELECT COUNT(*) FROM amazon_sales;

-- Data Analysis Using SQL
-- Top Rated Products 
SELECT product_name,
       rating
FROM amazon_sales
ORDER BY rating DESC
LIMIT 10;

-- Category-wise Average Rating
SELECT category,
       AVG(rating) AS avg_rating
FROM amazon_sales
GROUP BY category;

-- Highest Discount Products
SELECT product_name,
       discount_percentage
FROM amazon_sales
ORDER BY discount_percentage DESC;