USE sales_management;
-- Tạo index
CREATE INDEX idx_product_name
ON Products(ProductName);
#---check stock---
DROP TRIGGER IF EXISTS trg_check_stock;
DELIMITER $$

CREATE TRIGGER trg_check_stock
BEFORE INSERT ON OrderDetails
FOR EACH ROW
BEGIN
    DECLARE current_stock INT;

    SELECT StockQuantity INTO current_stock
    FROM Products
    WHERE ProductID = NEW.ProductID;

    IF current_stock < NEW.Quantity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Not enough stock';
    END IF;
END $$

DELIMITER ;

#---update stock( after insert)
DROP TRIGGER IF EXISTS trg_update_stock;

DELIMITER $$

CREATE TRIGGER trg_update_stock
AFTER INSERT ON OrderDetails
FOR EACH ROW
BEGIN
    UPDATE Products
    SET StockQuantity = StockQuantity - NEW.Quantity
    WHERE ProductID = NEW.ProductID;
END $$

DELIMITER ;

#----view---
DROP VIEW IF EXISTS SalesReport;

CREATE VIEW SalesReport AS
SELECT 
    o.OrderID,
    c.CustomerName,
    e.EmployeeName,
    p.ProductName,
    od.Quantity,
    od.SalePrice,
    (od.Quantity * od.SalePrice) AS TotalAmount
FROM OrderDetails od
JOIN Orders o ON od.OrderID = o.OrderID
JOIN Customers c ON o.CustomerID = c.CustomerID
JOIN Employees e ON o.EmployeeID = e.EmployeeID
JOIN Products p ON od.ProductID = p.ProductID;

#----fuction---
DROP FUNCTION IF EXISTS calculate_total;

DELIMITER $$

CREATE FUNCTION calculate_total(qty INT, price DECIMAL(10,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    RETURN qty * price;
END $$

DELIMITER ;

#----procedure---
DROP PROCEDURE IF EXISTS create_order;

DELIMITER $$

CREATE PROCEDURE create_order(
    IN c_id INT,
    IN e_id INT,
    IN p_id INT,
    IN qty INT,
    IN price DECIMAL(10,2)
)
BEGIN
    DECLARE new_order_id INT;

    -- tạo order
    INSERT INTO Orders(CustomerID, EmployeeID, OrderDate, Status)
    VALUES (c_id, e_id, CURDATE(), 'Pending');

    SET new_order_id = LAST_INSERT_ID();

    -- thêm order detail
    INSERT INTO OrderDetails(OrderID, ProductID, Quantity, SalePrice)
    VALUES (new_order_id, p_id, qty, price);
END $$

DELIMITER ;

#---test
SELECT * FROM SalesReport;
SELECT calculate_total(2, 500);
SELECT * FROM Products;
CALL create_order(1, 1, 5, 2, 20000);
SELECT * FROM Products;
SELECT * FROM Orders;
SELECT * FROM OrderDetails;
CALL create_order(1, 1, 1, 999, 20000); #nếu bán quá số lượng 



SELECT * FROM Customers;
SELECT * FROM Products;

SELECT * FROM Products WHERE ProductID = 5;


