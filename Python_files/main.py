from customer import add_customer, get_customers, update_customer, search_customer
from product import add_product, get_products, update_product, delete_product, update_stock
from order import create_order, update_order_status, get_orders
from employee import add_employee, get_employees, update_employee
from report import revenue_report, inventory_report, sales_by_employee_report, sales_detail_report

while True:
    print("\n" + "=" * 40)
    print("    SALES MANAGEMENT SYSTEM")
    print("=" * 40)
    print("  --- CUSTOMER ---")
    print("  1. Add Customer")
    print("  2. View Customers")
    print("  3. Update Customer")
    print("  4. Search Customer")
    print("  --- PRODUCT ---")
    print("  5. Add Product")
    print("  6. View Products")
    print("  7. Update Product")
    print("  8. Delete Product")
    print("  9. Update Stock")
    print("  --- ORDER ---")
    print("  10. Create Order")
    print("  11. View Orders")
    print("  12. Update Order Status")
    print("  --- EMPLOYEE ---")
    print("  13. Add Employee")
    print("  14. View Employees")
    print("  15. Update Employee")
    print("  --- REPORTS ---")
    print("  16. Revenue Report")
    print("  17. Inventory Report")
    print("  18. Sales by Employee Report")
    print("  19. Detailed Sales Report")
    print("  --- EXIT ---")
    print("  0. Exit")
    print("=" * 40)

    choice = input("Choose: ").strip()

    # --- CUSTOMER ---
    if choice == "1":
        name = input("Name: ")
        address = input("Address: ")
        phone = input("Phone: ")
        add_customer(name, address, phone)

    elif choice == "2":
        get_customers()

    elif choice == "3":
        get_customers()
        customer_id = int(input("Customer ID to update: "))
        name = input("New Name: ")
        address = input("New Address: ")
        phone = input("New Phone: ")
        update_customer(customer_id, name, address, phone)

    elif choice == "4":
        keyword = input("Search by name or phone: ")
        search_customer(keyword)

    # --- PRODUCT ---
    elif choice == "5":
        name = input("Product name: ")
        price = float(input("Price: "))
        stock = int(input("Stock: "))
        add_product(name, price, stock)

    elif choice == "6":
        get_products()

    elif choice == "7":
        get_products()
        product_id = int(input("Product ID to update: "))
        name = input("New Name: ")
        price = float(input("New Price: "))
        stock = int(input("New Stock: "))
        update_product(product_id, name, price, stock)

    elif choice == "8":
        get_products()
        product_id = int(input("Product ID to delete: "))
        confirm = input(f"Are you sure you want to delete product {product_id}? (yes/no): ")
        if confirm.lower() == "yes":
            delete_product(product_id)
        else:
            print("Cancelled.")

    elif choice == "9":
        get_products()
        product_id = int(input("Product ID to update stock: "))
        quantity = int(input("New stock quantity: "))
        update_stock(product_id, quantity)

    # --- ORDER ---
    elif choice == "10":
        get_customers()
        c_id = int(input("Customer ID: "))
        get_employees()
        e_id = int(input("Employee ID: "))
        get_products()
        p_id = int(input("Product ID: "))
        qty = int(input("Quantity: "))
        price = float(input("Sale Price: "))
        create_order(c_id, e_id, p_id, qty, price)

    elif choice == "11":
        get_orders()

    elif choice == "12":
        get_orders()
        order_id = int(input("Order ID: "))
        print("Status options: Pending / Completed / Cancelled")
        status = input("New Status: ")
        update_order_status(order_id, status)

    # --- EMPLOYEE ---
    elif choice == "13":
        name = input("Employee Name: ")
        job_title = input("Job Title: ")
        add_employee(name, job_title)

    elif choice == "14":
        get_employees()

    elif choice == "15":
        get_employees()
        employee_id = int(input("Employee ID to update: "))
        name = input("New Name: ")
        job_title = input("New Job Title: ")
        update_employee(employee_id, name, job_title)

    # --- REPORTS ---
    elif choice == "16":
        revenue_report()

    elif choice == "17":
        inventory_report()

    elif choice == "18":
        sales_by_employee_report()

    elif choice == "19":
        sales_detail_report()

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid choice! Please try again.")