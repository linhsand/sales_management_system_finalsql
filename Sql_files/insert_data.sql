USE sales_management;

-- =============================
-- INSERT CUSTOMERS 
-- =============================
INSERT INTO Customers (CustomerName, Address, PhoneNumber) VALUES
('Nguyen Van A', 'Hanoi', '0901111111'),
('Tran Thi B', 'Ho Chi Minh City', '0902222222'),
('Le Van C', 'Danang', '0903333333'),
('Pham Thi D', 'Hue', '0904444444'),
('Hoang Van E', 'Can Tho', '0905555555'),
('Bui Thi F', 'Hanoi', '0906666666'),
('Dang Van G', 'Hai Phong', '0907777777'),
('Vo Thi H', 'Nha Trang', '0908888888'),
('Nguyen Van I', 'Vung Tau', '0909999999'),
('Tran Van J', 'Hanoi', '0910101010'),
('Le Thi K', 'Ho Chi Minh City', '0911111112'),
('Pham Van L', 'Quang Ninh', '0912121212'),
('Hoang Thi M', 'Da Lat', '0913131313'),
('Do Van N', 'Binh Duong', '0914141414'),
('Ngo Thi O', 'Long An', '0915151515');

-- =============================
-- INSERT EMPLOYEES 
-- =============================
INSERT INTO Employees (EmployeeName, JobTitle) VALUES
('THUY NGAN', 'Sales'),
('HOANG VAN', 'Sales'),
('HUY ANH', 'Manager'),
('MINH TU', 'Sales'),
('BICH NGOC', 'Accountant'),
('QUOC HUNG', 'Sales'),
('THU HA', 'Sales Supervisor'),
('MINH KHOA', 'Sales');

-- =============================
-- INSERT PRODUCTS 
-- =============================
INSERT INTO Products (ProductName, Price, StockQuantity) VALUES
('Laptop', 20000, 15),
('Mouse', 200, 100),
('Keyboard', 500, 80),
('Monitor', 3000, 30),
('Headphone', 800, 50),
('Webcam', 600, 40),
('USB Hub', 300, 60),
('External SSD', 1500, 25),
('Laptop Stand', 400, 45),
('Mousepad', 100, 120),
('HDMI Cable', 150, 90),
('Desk Lamp', 250, 35);

-- =============================
-- INSERT ORDERS 
-- =============================
INSERT INTO Orders (CustomerID, EmployeeID, OrderDate, Status) VALUES
(1, 1, CURDATE(), 'Completed'),
(2, 2, CURDATE(), 'Completed'),
(3, 1, CURDATE(), 'Pending'),
(4, 3, CURDATE(), 'Completed'),
(5, 2, CURDATE(), 'Cancelled'),
(6, 4, CURDATE(), 'Completed'),
(7, 1, CURDATE(), 'Pending'),
(8, 5, CURDATE(), 'Completed'),
(9, 6, CURDATE(), 'Completed'),
(10, 2, CURDATE(), 'Pending'),
(11, 7, CURDATE(), 'Completed'),
(12, 1, CURDATE(), 'Cancelled'),
(13, 4, CURDATE(), 'Completed'),
(14, 8, CURDATE(), 'Pending'),
(15, 3, CURDATE(), 'Completed'),
(1, 6, CURDATE(), 'Completed'),
(3, 2, CURDATE(), 'Pending'),
(5, 7, CURDATE(), 'Completed'),
(7, 1, CURDATE(), 'Completed'),
(9, 4, CURDATE(), 'Cancelled');

-- =============================
-- INSERT ORDER DETAILS 
-- =============================
INSERT INTO OrderDetails (OrderID, ProductID, Quantity, SalePrice) VALUES
(1, 1, 1, 20000),
(1, 2, 2, 200),
(2, 3, 1, 500),
(2, 5, 1, 800),
(3, 4, 1, 3000),
(3, 6, 2, 600),
(4, 2, 3, 200),
(4, 7, 1, 300),
(5, 3, 2, 500),
(6, 1, 1, 20000),
(6, 8, 1, 1500),
(7, 9, 2, 400),
(7, 10, 3, 100),
(8, 11, 2, 150),
(8, 12, 1, 250),
(9, 2, 5, 200),
(9, 3, 2, 500),
(10, 4, 1, 3000),
(10, 5, 2, 800),
(11, 1, 2, 20000),
(11, 6, 1, 600),
(12, 7, 3, 300),
(13, 8, 1, 1500),
(13, 9, 2, 400),
(14, 10, 4, 100),
(14, 11, 3, 150),
(15, 12, 2, 250),
(15, 2, 4, 200),
(16, 3, 3, 500),
(16, 5, 1, 800),
(17, 4, 2, 3000),
(17, 6, 1, 600),
(18, 1, 1, 20000),
(18, 7, 2, 300),
(19, 8, 1, 1500),
(19, 9, 3, 400),
(20, 10, 2, 100),
(20, 11, 1, 150),
(1, 12, 2, 250),
(2, 10, 5, 100);

-- =============================
-- VERIFY
-- =============================
SELECT COUNT(*) AS total_customers FROM Customers;
SELECT COUNT(*) AS total_employees FROM Employees;
SELECT COUNT(*) AS total_products FROM Products;
SELECT COUNT(*) AS total_orders FROM Orders;
SELECT COUNT(*) AS total_order_details FROM OrderDetails;



