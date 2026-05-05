from db_connection import get_connection

def revenue_report():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT SUM(Quantity * SalePrice) AS Revenue
    FROM OrderDetails
    """
    cursor.execute(query)
    result = cursor.fetchone()

    print(f"\n{'='*40}")
    print(f"  TOTAL REVENUE REPORT")
    print(f"{'='*40}")
    print(f"  Total Revenue: {result[0]:,.2f}" if result[0] else "  Total Revenue: 0.00")
    print(f"{'='*40}")

    conn.close()

def inventory_report():
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT ProductID, ProductName, Price, StockQuantity FROM Products ORDER BY StockQuantity ASC"
    cursor.execute(query)
    result = cursor.fetchall()

    print(f"\n{'='*55}")
    print(f"  INVENTORY REPORT")
    print(f"{'='*55}")
    print(f"{'ID':<5} {'Product':<20} {'Price':<12} {'Stock':<10}")
    print("-" * 55)
    for row in result:
        stock_warning = " ⚠ LOW" if row[3] < 5 else ""
        print(f"{row[0]:<5} {row[1]:<20} {float(row[2]):<12.2f} {row[3]:<10}{stock_warning}")
    print(f"{'='*55}")

    conn.close()

def sales_by_employee_report():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT e.EmployeeName,
           COUNT(DISTINCT o.OrderID) AS TotalOrders,
           SUM(od.Quantity * od.SalePrice) AS TotalRevenue
    FROM Employees e
    JOIN Orders o ON e.EmployeeID = o.EmployeeID
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    GROUP BY e.EmployeeID, e.EmployeeName
    ORDER BY TotalRevenue DESC
    """
    cursor.execute(query)
    result = cursor.fetchall()

    print(f"\n{'='*55}")
    print(f"  SALES BY EMPLOYEE REPORT")
    print(f"{'='*55}")
    print(f"{'Employee':<20} {'Orders':<10} {'Revenue':<15}")
    print("-" * 55)
    for row in result:
        print(f"{row[0]:<20} {row[1]:<10} {float(row[2]):<15.2f}")
    print(f"{'='*55}")

    conn.close()

def sales_detail_report():
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM SalesReport"
    cursor.execute(query)
    result = cursor.fetchall()

    print(f"\n{'='*90}")
    print(f"  DETAILED SALES REPORT")
    print(f"{'='*90}")
    print(f"{'OrderID':<10} {'Customer':<18} {'Employee':<18} {'Product':<15} {'Qty':<6} {'Price':<10} {'Total':<10}")
    print("-" * 90)
    for row in result:
        print(f"{row[0]:<10} {row[1]:<18} {row[2]:<18} {row[3]:<15} {row[4]:<6} {float(row[5]):<10.2f} {float(row[6]):<10.2f}")
    print(f"{'='*90}")

    conn.close()