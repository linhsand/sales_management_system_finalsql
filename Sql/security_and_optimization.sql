USE sales_management;

-- =============================
-- USER ACCOUNTS & ROLES
-- =============================

-- Admin user: full access
CREATE USER IF NOT EXISTS 'admin_user'@'localhost' IDENTIFIED BY 'admin123';

-- Normal user: limited access
CREATE USER IF NOT EXISTS 'normal_user'@'localhost' IDENTIFIED BY 'user123';

-- Grant admin full privileges
GRANT ALL PRIVILEGES ON sales_management.*
TO 'admin_user'@'localhost';

-- Grant normal user read + insert only
GRANT SELECT, INSERT
ON sales_management.*
TO 'normal_user'@'localhost';

FLUSH PRIVILEGES;

-- =============================
-- QUERY OPTIMIZATION
-- =============================

-- Index on ProductName for fast product search
CREATE INDEX IF NOT EXISTS idx_product_name
ON Products(ProductName);

-- Index on Orders.CustomerID for fast customer order lookup
CREATE INDEX IF NOT EXISTS idx_orders_customer
ON Orders(CustomerID);

-- Index on OrderDetails.OrderID for fast detail lookup
CREATE INDEX IF NOT EXISTS idx_orderdetails_order
ON OrderDetails(OrderID);

-- Check query execution plan
EXPLAIN
SELECT * FROM Products
WHERE ProductName = 'Laptop';

-- =============================
-- BACKUP & DISASTER RECOVERY
-- =============================
-- Run the following commands in your terminal (outside MySQL):

-- BACKUP the entire database:
-- mysqldump -u root -p sales_management > backup_sales_management.sql

-- BACKUP with date in filename (recommended):
-- mysqldump -u root -p sales_management > backup_$(date +%Y%m%d).sql

-- RESTORE from backup:
-- mysql -u root -p sales_management < backup_sales_management.sql

-- SCHEDULED BACKUP (Linux crontab - runs daily at 2am):
-- 0 2 * * * mysqldump -u root -pYOURPASSWORD sales_management > /backups/backup_$(date +\%Y\%m\%d).sql

-- =============================
-- SECURITY MEASURES (Summary)
-- =============================
-- 1. Role-based access: admin vs normal user with different privileges
-- 2. Use strong passwords for all database users
-- 3. Never use root for application connections
-- 4. Use prepared statements in Python to prevent SQL injection
-- 5. Regularly back up the database using mysqldump
-- 6. Store backups in a separate location from the server