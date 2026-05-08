USE sales_management;

-- =============================
-- INSERT CUSTOMERS (5 records)
-- =============================
INSERT INTO Customers (CustomerName, Address, PhoneNumber) VALUES
('Nguyen Van A', 'Hanoi', '0901'),
('Tran Thi B', 'HCM', '0902'),
('Le Van C', 'Danang', '0903'),
('Pham Thi D', 'Hue', '0904'),
('Hoang Van E', 'Can Tho', '0905');

-- =============================
-- INSERT EMPLOYEES (5 records)
-- =============================
INSERT INTO Employees (EmployeeName, JobTitle) VALUES
('THUY NGAN', 'Sales'),
('HOANG VAN', 'Sales'),
('HUY ANH', 'Manager'),
('MINH TU', 'Sales'),
('BICH NGOC', 'Accountant');

-- =============================
-- INSERT PRODUCTS (5 records)
-- =============================
INSERT INTO Products (ProductName, Price, StockQuantity) VALUES
('Laptop', 20000, 10),
('Mouse', 200, 50),
('Keyboard', 500, 30),
('Monitor', 3000, 20),
('Headphone', 800, 25);

-- =============================
-- INSERT ORDERS (5 records)
-- =============================
INSERT INTO Orders (CustomerID, EmployeeID, OrderDate, Status) VALUES
(1, 1, CURDATE(), 'Pending'),
(2, 2, CURDATE(), 'Completed'),
(3, 1, CURDATE(), 'Pending'),
(4, 3, CURDATE(), 'Completed'),
(5, 2, CURDATE(), 'Cancelled');

-- =============================
-- INSERT ORDER DETAILS (7 records)
-- =============================
INSERT INTO OrderDetails (OrderID, ProductID, Quantity, SalePrice) VALUES
(1, 1, 1, 20000),
(1, 2, 2, 200),
(2, 3, 1, 500),
(3, 4, 1, 3000),
(3, 5, 2, 800),
(4, 2, 3, 200),
(5, 3, 2, 500);

-- =============================
-- VERIFY
-- =============================
SELECT * FROM Customers;
SELECT * FROM Employees;
SELECT * FROM Products;
SELECT * FROM Orders;
SELECT * FROM OrderDetails;
