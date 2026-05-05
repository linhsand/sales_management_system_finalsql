from db_connection import get_connection

def create_order(customer_id, employee_id, product_id, quantity, price):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.callproc("create_order", [customer_id, employee_id, product_id, quantity, price])

    conn.commit()
    conn.close()
    print("Order created successfully!")

def update_order_status(order_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE Orders SET Status = %s WHERE OrderID = %s"
    cursor.execute(query, (status, order_id))

    conn.commit()
    conn.close()
    print("Order status updated!")

def get_orders():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT o.OrderID, c.CustomerName, e.EmployeeName, o.OrderDate, o.Status
    FROM Orders o
    JOIN Customers c ON o.CustomerID = c.CustomerID
    JOIN Employees e ON o.EmployeeID = e.EmployeeID
    ORDER BY o.OrderID
    """
    cursor.execute(query)
    result = cursor.fetchall()

    if not result:
        print("No orders found.")
    else:
        print(f"\n{'ID':<5} {'Customer':<20} {'Employee':<20} {'Date':<12} {'Status':<12}")
        print("-" * 70)
        for row in result:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<20} {str(row[3]):<12} {row[4]:<12}")

    conn.close()