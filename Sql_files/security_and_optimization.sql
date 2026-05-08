USE sales_management;

-- =============================
-- USER ACCOUNTS & ROLES
-- =============================

CREATE USER IF NOT EXISTS 'admin_user'@'localhost' IDENTIFIED BY 'admin123';
CREATE USER IF NOT EXISTS 'normal_user'@'localhost' IDENTIFIED BY 'user123';

GRANT ALL PRIVILEGES ON sales_management.*
TO 'admin_user'@'localhost';

GRANT SELECT, INSERT
ON sales_management.*
TO 'normal_user'@'localhost';

FLUSH PRIVILEGES;

-- =============================
-- QUERY OPTIMIZATION
-- =============================

EXPLAIN
SELECT * FROM Products
WHERE ProductName = 'Laptop';

-- =============================
-- BACKUP & DISASTER RECOVERY
-- =============================

-- BACKUP the entire database:
-- mysqldump -u root -p sales_management > backup_sales_management.sql

-- BACKUP with date in filename (recommended):
-- mysqldump -u root -p sales_management > backup_YYYYMMDD.sql

-- RESTORE from backup:
-- mysql -u root -p sales_management < backup_sales_management.sql

-- =============================
-- SECURITY MEASURES (Summary)
-- =============================
-- 1. Role-based access: admin vs normal user with different privileges
-- 2. Use strong passwords for all database users
-- 3. Never use root for application connections
-- 4. Use prepared statements in Python to prevent SQL injection
-- 5. Regularly back up the database using mysqldump
-- 6. Store backups in a separate location from the server
