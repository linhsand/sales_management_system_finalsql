from db_connection import get_connection

def add_customer(name, address, phone):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO Customers (CustomerName, Address, PhoneNumber) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, address, phone))

    conn.commit()
    conn.close()
    print("Customer added successfully!")

def get_customers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Customers")
    result = cursor.fetchall()

    if not result:
        print("No customers found.")
    else:
        print(f"\n{'ID':<5} {'Name':<20} {'Address':<20} {'Phone':<15}")
        print("-" * 60)
        for row in result:
            print(f"{row[0]:<5} {row[1]:<20} {str(row[2]):<20} {str(row[3]):<15}")

    conn.close()

def update_customer(customer_id, name, address, phone):
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE Customers SET CustomerName=%s, Address=%s, PhoneNumber=%s WHERE CustomerID=%s"
    cursor.execute(query, (name, address, phone, customer_id))

    conn.commit()
    conn.close()
    print("Customer updated successfully!")

def search_customer(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM Customers WHERE CustomerName LIKE %s OR PhoneNumber LIKE %s"
    cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
    result = cursor.fetchall()

    if not result:
        print("No customers found.")
    else:
        print(f"\n{'ID':<5} {'Name':<20} {'Address':<20} {'Phone':<15}")
        print("-" * 60)
        for row in result:
            print(f"{row[0]:<5} {row[1]:<20} {str(row[2]):<20} {str(row[3]):<15}")

    conn.close()