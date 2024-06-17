-- 1. What are the top 5 products by sales volume?
SELECT ProductName
FROM ecommerce_sales
ORDER BY Sales DESC
LIMIT 5;

-- 2. Which category has the highest average price?
SELECT Category, AVG(Price)
FROM ecommerce_sales
GROUP BY 1
ORDER BY 2 DESC;

-- 3. How many products are there in each category?
SELECT Category, COUNT(ProductName) product_count
FROM ecommerce_sales
GROUP BY 1;

-- 4. What is the average rating for each category?
SELECT Category, AVG(Rating) avg_rating
FROM ecommerce_sales
GROUP BY 1
ORDER BY 2 DESC;

-- 5. Which products have a rating above 4.0 and more than 1000 reviews?
SELECT ProductName
FROM ecommerce_sales
WHERE Rating > 4.0 AND NumReviews > 1000;

-- 6. What is the total revenue generated (price * sales) for each category?
SELECT Category, ROUND(SUM(price * sales),2) AS revenue
FROM ecommerce_sales
GROUP BY 1
ORDER BY 2 DESC;

-- 7. How many products were added to the inventory each month?
SELECT MONTHNAME(Date_Added) months, COUNT(ProductName) counts
FROM ecommerce_sales
GROUP BY 1
ORDER BY 1;

-- 8. Which products have less than 100 items left in stock?
SELECT ProductName, COUNT(*)
FROM ecommerce_sales
GROUP BY 1
HAVING COUNT(*) < 100;

-- 9. What is the average discount percentage for each category?
SELECT Category, ROUND(AVG(Discount) * 100,2) avg_discount
FROM ecommerce_sales
GROUP BY 1;

-- 10. Who are the top 10 bestselling products with their names and sales figures?
SELECT ProductName, Sales
FROM ecommerce_sales
ORDER BY 2 DESC
LIMIT 10;

-- 11. How does the average price of products vary by category and rating (rounded to the nearest integer)?
SELECT Category, Rating, ROUND(AVG(Price)) AS average_price
FROM ecommerce_sales
GROUP BY category, rating
ORDER BY category, rating;

-- 12. For each category, what is the product with the highest revenue (price * sales)?
WITH CTE AS (SELECT Category, ProductName, ROUND((Price * Sales),2)
 as revenue,
ROW_NUMBER() OVER (PARTITION BY Category ORDER BY (Price * Sales) DESC) rn
FROM ecommerce_sales)
SELECT Category, ProductName, revenue 
FROM CTE
WHERE rn = 1;




