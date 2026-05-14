# Sales Management System

**Project 03 — Database Management System**
National Economics University 
---

## Project Information

| Field | Details |
|---|---|
| Project Title | Sales Management System |
| Course | Database Management System (MySQL) |
| Institution | National Economics University (NEU) |
| Instructor | TRAN HUNG |
| Student Name | Vu Tran Cat Linh |
| Student ID | 11245899 |
| Class | DSEB 66B |

| Academic Year | 2025 – 2026 |
| GitHub | https://github.com/linhsand/sales_management_system_finalsql |
| Youtube (video demo) | _____link___ |


---

## Overview

This project is a comprehensive Sales Management System that integrates a MySQL relational database with a Python application. It is designed to manage customers, products, orders, employees, and generate sales reports through both a graphical interface (GUI) and a command-line interface (CLI).

The system demonstrates real-world database concepts including stored procedures, triggers, views, user-defined functions, indexes, and role-based security — all connected to a Python frontend.

---

## Features

**Customer Management**
- Register new customers
- Update customer information
- Search by name or phone number

**Product Management**
- Add, edit, and delete products
- Update stock inventory manually

**Order Management**
- Create orders using a stored procedure
- Update order status (Pending / Completed / Cancelled)
- View all orders with customer and employee details

**Employee Management**
- Add and update employee records and job titles

**Reports & Analytics**
- Total revenue report (using UDF `calculate_total`)
- Inventory report with low-stock warnings
- Sales breakdown by employee
- Detailed sales report (using `SalesReport` view)
- Daily orders report (using `DailyOrders` view)

**Advanced Database Features**
- 3 indexes for query optimization
- 2 views: `SalesReport`, `DailyOrders`
- 1 stored procedure: `create_order`
- 1 user-defined function: `calculate_total`
- 2 triggers: `trg_check_stock`, `trg_update_stock`
- Role-based user accounts: `admin_user`, `normal_user`

---

## Technology Stack

| Component | Technology |
|---|---|
| Database | MySQL 8.x |
| Programming Language | Python 3.11 |
| Database Connector | mysql-connector-python |
| GUI Framework | tkinter (built-in) |
| CLI Interface | Python standard input |
| Design Tools | MySQL Workbench, ERDPlus |

---

## Repository Structure

```
sales_management_system_finalsql/
│
├── Python_files/
│   ├── db_connection.py       # Database connection configuration
│   ├── customer.py            # Customer CRUD operations
│   ├── product.py             # Product CRUD operations
│   ├── order.py               # Order management
│   ├── employee.py            # Employee management
│   ├── report.py              # Report generation
│   ├── main.py                # Command-line interface (19 options)
│   └── gui.py                 # Graphical user interface (7 pages)
│
├── SQL_files/
│   ├── schema.sql             # Database and table creation
│   ├── insert_data.sql        # Sample data

│   ├── advanced.sql           # Indexes, triggers, views, UDF, procedure
│   └── security_and_optimization.sql  # Users, roles, EXPLAIN
│
├── Diagrams/
│   ├── er_diagram.mwb         # MySQL Workbench physical EER diagram
│   └── erdplus_er_diagram.png # Conceptual ER diagram (ERDPlus)
│
└── README.md
```

---

## Prerequisites

Make sure you have the following installed before starting:

- [MySQL 8.x](https://dev.mysql.com/downloads/mysql/) — database server
- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) — to run SQL files
- [Python 3.11+](https://www.python.org/downloads/) — to run the application
- mysql-connector-python — Python library to connect to MySQL

Install the Python library by running this in your terminal:

```bash
pip install mysql-connector-python
```

---

## Setup Instructions

### Step 1 — Configure the database connection

Open `Python_files/db_connection.py` and update the credentials to match your MySQL setup:

```python
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="240506",   
        database="sales_management"
    )
```

---

### Step 2 — Set up the database in MySQL Workbench

Open MySQL Workbench and connect to your local MySQL server. Then run the SQL files **in this exact order**:

**1. Create the database and tables**
```
Open SQL_files/schema.sql → Run with Ctrl + Shift + Enter
```

**2. Insert sample data**
```
Open SQL_files/insert_data.sql → Run with Ctrl + Shift + Enter
```

**3. Create advanced database objects**
```
Open SQL_files/advanced.sql → Run with Ctrl + Shift + Enter
```
This creates: 3 indexes, 2 triggers, 2 views (`SalesReport`, `DailyOrders`), 1 function (`calculate_total`), 1 procedure (`create_order`)

**4. Set up users and security**
```
Open SQL_files/security_and_optimization.sql → Run with Ctrl + Shift + Enter
```
This creates `admin_user` (full access) and `normal_user` (read/insert only)

---

### Step 3 — Run the application

Navigate to the `Python_files` folder in your terminal:

```bash
cd Python_files
```

**To launch the Graphical User Interface (GUI):**
```bash
python gui.py
```

**To launch the Command-Line Interface (CLI):**
```bash
python main.py
```

---

## GUI Pages

The graphical interface has 7 pages accessible from the sidebar:

| Page | Description |
|---|---|
| Dashboard | Live statistics — total customers, products, orders, revenue |
| Customers | Add, update, search customers |
| Products | Add, update, delete products and manage stock |
| Orders | Create orders, update status, view order list |
| Employees | Add and update employee records |
| Reports | Revenue, inventory, by-employee, daily orders, detailed sales |
| Advanced DB | Live demo of all 5 advanced database features |

---

## Database Schema

```
Customers     (CustomerID, CustomerName, Address, PhoneNumber)
Products      (ProductID, ProductName, Price, StockQuantity)
Employees     (EmployeeID, EmployeeName, JobTitle)
Orders        (OrderID, CustomerID*, EmployeeID*, OrderDate, Status)
OrderDetails  (OrderDetailID, OrderID*, ProductID*, Quantity, SalePrice)
```

`*` = Foreign Key

---

## Advanced Database Objects

| Object | Name | Purpose |
|---|---|---|
| Index | idx_product_name | Fast product search by name |
| Index | idx_orders_customer | Fast order lookup by customer |
| Index | idx_orderdetails_order | Fast detail lookup by order |
| View | SalesReport | Full sales report joining 5 tables |
| View | DailyOrders | Orders placed today with totals |
| Procedure | create_order | Atomic order creation across 2 tables |
| Function | calculate_total | Computes line total: qty × price |
| Trigger | trg_check_stock | Blocks orders that exceed stock (BEFORE INSERT) |
| Trigger | trg_update_stock | Reduces stock automatically (AFTER INSERT) |

---

## Sample Data

Each table contains 5–7 representative records:

- **5 Customers** — from Hanoi, HCM, Danang, Hue, Can Tho
- **5 Employees** — roles include Sales, Manager, Accountant
- **5 Products** — Laptop, Mouse, Keyboard, Monitor, Headphone
- **5 Orders** — mix of Pending, Completed, Cancelled statuses
- **7 Order Details** — multiple products per order

---

## Security

| User | Privileges | Purpose |
|---|---|---|
| admin_user | ALL PRIVILEGES | Database administration |
| normal_user | SELECT, INSERT | Application usage |

All Python queries use parameterized statements to prevent SQL injection. The root account is not used for application connections.

---

## Backup

To back up the database, run this command in your terminal:

```bash
mysqldump -u root -p sales_management > backup_sales_management.sql
```

To restore:

```bash
mysql -u root -p sales_management < backup_sales_management.sql
```

---

## References

- Oracle Corporation. (2024). MySQL 8.0 Reference Manual. https://dev.mysql.com/doc/refman/8.0/en/
- Python Software Foundation. (2024). Python 3.11 Documentation. https://docs.python.org/3/
- Oracle Corporation. (2024). MySQL Connector/Python Developer Guide. https://dev.mysql.com/doc/connector-python/en/
- ERDPlus. (2024). ER Diagram Tool. https://erdplus.com/
- Oracle Corporation. (2024). MySQL Workbench Manual. https://dev.mysql.com/doc/workbench/en/

---

*Project 03 — Sales Management System · NEU College of Technology · May 2026*
