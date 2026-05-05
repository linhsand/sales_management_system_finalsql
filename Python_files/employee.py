from db_connection import get_connection

def add_employee(name, job_title):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO Employees (EmployeeName, JobTitle) VALUES (%s, %s)"
    cursor.execute(query, (name, job_title))

    conn.commit()
    conn.close()
    print("Employee added successfully!")

def get_employees():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Employees")
    result = cursor.fetchall()

    if not result:
        print("No employees found.")
    else:
        print(f"\n{'ID':<5} {'Name':<20} {'Job Title':<20}")
        print("-" * 45)
        for row in result:
            print(f"{row[0]:<5} {row[1]:<20} {str(row[2]):<20}")

    conn.close()

def update_employee(employee_id, name, job_title):
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE Employees SET EmployeeName=%s, JobTitle=%s WHERE EmployeeID=%s"
    cursor.execute(query, (name, job_title, employee_id))

    conn.commit()
    conn.close()
    print("Employee updated successfully!")