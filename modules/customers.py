import os
from modules.database import connect
from psycopg import errors


def create_customer(name, cpf=None, phone=None, email=None):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = """
                INSERT INTO customers (name, cpf, phone, email)
                VALUES (%s, %s, %s, %s)
                """
                values = (name, cpf, phone, email)
                cur.execute(query, values)
        print(f"Customer '{name}' created!")
    except errors.UniqueViolation:
        print("Error: CPF already registered!")
    except Exception as e:
        print(f"Error: {e}")


def list_customers():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = "SELECT * FROM customers"
                cur.execute(query)
                customers = cur.fetchall()

                if not customers:
                    print("No customers found.")
                    
                print("\n=== Customers ===")
                for customer in customers:
                    customer_id, name, cpf, phone, email = customer
                    print(
                        f"""
ID: {customer_id}
Name: {name}
CPF: {cpf or 'N/A'}
Phone: {phone or 'N/A'}
Email: {email or 'N/A'}
{'-' * 30}
"""
                    )
    except Exception as e:
        print(f"Error: {e}")


def update_customer(id, name, cpf, phone, email):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = """
                    UPDATE customers
                    SET name = %s, cpf = %s, phone = %s, email = %s
                    WHERE id = %s
                    """
                values = (name, cpf, phone, email, id)
                cur.execute(query, values)
        print("Customer updated!")
    except errors.UniqueViolation:
        print("Error: CPF already registered!")
    except Exception as e:
        print(f"Error: {e}")


def delete_customer(id):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = "DELETE FROM customers WHERE id = %s"
                values = (id,)
                cur.execute(query, values)
        print("Customer deleted!")
    except errors.ForeignKeyViolation:
        print("Error: customer has sales — cannot delete!")
    except Exception as e:
        print(f"Error: {e}")


def menu_customers():
    while True:
        print("=== CUSTOMERS ===")
        print("1 - List customers")
        print("2 - Create customer")
        print("3 - Update customer")
        print("4 - Delete customer")
        print("0 - Back")

        option = input("\nChoose: ")
        os.system("clear")

        match option:
            case "1":
                list_customers()
            case "2":
                name = input("Name: ")
                cpf = input("CPF (leave blank to skip): ").strip() or None
                phone = input("Phone (leave blank to skip): ").strip() or None
                email = input("Email (leave blank to skip): ").strip() or None
                create_customer(name, cpf, phone, email)
            case "3":
                list_customers()
                id = int(input("ID: "))
                name = input("New name: ")
                cpf = input("New CPF (leave blank to skip): ").strip() or None
                phone = input("New phone (leave blank to skip): ").strip() or None
                email = input("New email (leave blank to skip): ").strip() or None
                update_customer(id, name, cpf, phone, email)
            case "4":
                list_customers()
                id = int(input("ID: "))
                delete_customer(id)
            case "0":
                print("Going back...")
                break
            case _:
                print("Invalid option!")
