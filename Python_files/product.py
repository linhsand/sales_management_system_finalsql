from db_connection import get_connection

def add_product(name, price, stock):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO Products (ProductName, Price, StockQuantity) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, price, stock))

    conn.commit()
    conn.close()
    print("Product added successfully!")

def get_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Products")
    result = cursor.fetchall()

    if not result:
        print("No products found.")
    else:
        print(f"\n{'ID':<5} {'Name':<20} {'Price':<12} {'Stock':<10}")
        print("-" * 50)
        for row in result:
            print(f"{row[0]:<5} {row[1]:<20} {float(row[2]):<12.2f} {row[3]:<10}")

    conn.close()

def update_product(product_id, name, price, stock):
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE Products SET ProductName=%s, Price=%s, StockQuantity=%s WHERE ProductID=%s"
    cursor.execute(query, (name, price, stock, product_id))

    conn.commit()
    conn.close()
    print("Product updated successfully!")

def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM Products WHERE ProductID=%s"
    cursor.execute(query, (product_id,))

    conn.commit()
    conn.close()
    print("Product deleted successfully!")

def update_stock(product_id, quantity):
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE Products SET StockQuantity=%s WHERE ProductID=%s"
    cursor.execute(query, (quantity, product_id))

    conn.commit()
    conn.close()
    print("Stock updated successfully!")