USE sales_management;

-- =============================
-- INDEXES
-- =============================

CREATE INDEX idx_product_name ON Products(ProductName);
CREATE INDEX idx_orders_customer ON Orders(CustomerID);
CREATE INDEX idx_orderdetails_order ON OrderDetails(OrderID);

-- =============================
-- TRIGGERS
-- =============================

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

-- =============================
-- VIEWS
-- =============================

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

DROP VIEW IF EXISTS DailyOrders;

CREATE VIEW DailyOrders AS
SELECT
    o.OrderID,
    c.CustomerName,
    e.EmployeeName,
    o.OrderDate,
    o.Status,
    SUM(od.Quantity * od.SalePrice) AS TotalAmount
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
JOIN Employees e ON o.EmployeeID = e.EmployeeID
JOIN OrderDetails od ON o.OrderID = od.OrderID
WHERE o.OrderDate = CURDATE()
GROUP BY o.OrderID, c.CustomerName, e.EmployeeName, o.OrderDate, o.Status;

-- =============================
-- USER DEFINED FUNCTION
-- =============================

DROP FUNCTION IF EXISTS calculate_total;

DELIMITER $$

CREATE FUNCTION calculate_total(qty INT, price DECIMAL(10,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    RETURN qty * price;
END $$

DELIMITER ;

-- =============================
-- STORED PROCEDURE
-- =============================

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

    INSERT INTO Orders(CustomerID, EmployeeID, OrderDate, Status)
    VALUES (c_id, e_id, CURDATE(), 'Pending');

    SET new_order_id = LAST_INSERT_ID();

    INSERT INTO OrderDetails(OrderID, ProductID, Quantity, SalePrice)
    VALUES (new_order_id, p_id, qty, price);
END $$

DELIMITER ;

-- =============================
-- VERIFY
-- =============================

SELECT * FROM SalesReport;
SELECT * FROM DailyOrders;
SELECT calculate_total(2, 500);