import os
from modules.database import connect
from psycopg import errors


def create_employee(name, cpf, role_id, bonus_salary=0):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = """
                INSERT INTO employees (name, cpf, role_id, bonus_salary)
                VALUES (%s, %s, %s, %s)
                """
                values = (name, cpf, role_id, bonus_salary)
                cur.execute(query, values)
        print(f"Employee '{name}' created sucessfully!")

    except errors.UniqueViolation:
        print("Error: CPF already registered!")
    except errors.ForeignKeyViolation:
        print("Error: role not found!")
    except Exception as e:
        print(f"Error: {e}")


def list_employees():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = """
                SELECT
                e.id,
                e.name,
                e.cpf,
                r.name AS role,
                r.base_salary,
                e.bonus_salary,
                r.base_salary + e.bonus_salary AS total_salary
                FROM employees e
                JOIN roles r ON e.role_id = r.id
                ORDER BY e.name
                """
                cur.execute(query)
                employees = cur.fetchall()

                if not employees:
                    print("No employees found.")
                    return

                print("\n=== EMPLOYEES ===")
                for employee in employees:
                    employee_id, name, cpf, role, base_salary, bonus_salary, total_salary = employee
                    print(
                        f"""
ID: {employee_id}
Name: {name}
CPF: {cpf}
Role: {role}
Base Salary: {base_salary:.2f}
Bonus Salary: {bonus_salary:.2f}
Total Salary: {total_salary:.2f}
{'-' * 30}"""
                    )
    except Exception as e:
        print(f"Error: {e}")


def update_employee(id, name, cpf, role_id, bonus_salary):
    try:
        with connect() as conn:
            with conn.cursor as cur:
                query = """
                UPDATE employees
                SET name = %s, cpf = %s, role_id = %s, bonus_salary = %s
                WHERE id = %s
                """
                values = (id, name, cpf, role_id, bonus_salary)
                cur.execute(query, values)

        print("Employee updated successfully!")

    except errors.UniqueViolation:
        print("Error: CPF already registered!")
    except errors.ForeignKeyViolation:
        print("Error: role not found!")
    except Exception as e:
        print(f"Error: {e}")


def delete_employee(id):
    try:
        with connect() as conn:
            with conn.cursor as cur:
                query = "DELETE FROM employees WHERE id = %s"
                values = (id,)
                cur.execute(query, values)
        print("Employee deleted successfully!")

    except errors.ForeignKeyViolation:
        print("Error: employee has sales registered - cannot delete!")
    except Exception as e:
        print(f"Error: {e}")


def menu_employees():
    while True:
        print("\n=== EMPLOYEES ===")
        print("1 - List employees")
        print("2 - Create employee")
        print("3 - Update employee")
        print("4 - Delete employee")
        print("0 - Back")

        option = input("\nChoose: ")
        os.system("clear")

        match option:
            case "1":
                list_employees()

            case "2":
                list_employees()
                name = input("Name: ")
                cpf = input("CPF: ")
                role_id = int(input("Role ID: "))
                bonus_input = input("Bonus salary (leave blank for 0): ").strip()
                bonus_salary = float(bonus_input) if bonus_input else 0
                create_employee(name, cpf, role_id, bonus_salary)

            case "3":
                list_employees()
                id = int(input("Employee ID: "))
                name = input("New name: ")
                cpf = input("New CPF: ")
                role_id = int(input("New role ID: "))
                bonus_input = input("New bonus salary: ").strip()
                bonus_salary = float(bonus_input) if bonus_input else 0
                update_employee(id, name, cpf, role_id, bonus_salary)

            case "4":
                list_employees()
                id = int(input("Employee ID: "))
                delete_employee(id)

            case "0":
                break

            case _:
                print("Invalid option!")
