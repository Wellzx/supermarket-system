import os
from modules.database import connect
from psycopg import errors


def create_supplier(name, phone, email):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = "INSERT INTO suppliers (name, phone, email) VALUES (%s, %s, %s)"
                values = (name, phone, email)
                cur.execute(query, values)
        print(f"Supplier '{name}' created!")
    except errors.CheckViolation:
        print("Error: phone or email is required!")
    except Exception as e:
        print(f"Error: {e}")


def list_suppliers():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM suppliers")
                suppliers = cur.fetchall()
                if not suppliers:
                    print("No suppliers found.")
                    return
                for supplier in suppliers:
                    print(
                        f"ID: {supplier[0]} | Name: {supplier[1]} | Phone: {supplier[2]} | Email: {supplier[3]}"
                    )
    except Exception as e:
        print(f"Error: {e}")


def update_supplier(id, name, phone, email):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = "UPDATE suppliers SET name = %s, phone = %s, email = %s WHERE id = %s"
                values = (name, phone, email, id)
                cur.execute(query, values)
        print("Supplier updated!")
    except errors.CheckViolation:
        print("Error: phone or email is required!")
    except Exception as e:
        print(f"Error: {e}")


def delete_supplier(id):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = "DELETE FROM suppliers WHERE id = %s"
                values = (id,)
                cur.execute(query, values)
        print("Supplier deleted!")
    except errors.ForeignKeyViolation:
        print("Error: supplier has products — cannot delete!")
    except Exception as e:
        print(f"Error: {e}")


def menu_suppliers():
    while True:
        print("\n=== SUPPLIERS ===")
        print("1 - List suppliers")
        print("2 - Create supplier")
        print("3 - Update supplier")
        print("4 - Delete supplier")
        print("0 - Back")

        option = input("\nChoose: ")
        os.system("clear")

        match option:
            case "1":
                list_suppliers()
            case "2":
                name = input("Name: ")
                phone = input("Phone (leave blank to skip): ").strip() or None
                email = input("Email (leave blank to skip): ").strip() or None
                create_supplier(name, phone, email)
            case "3":
                list_suppliers()
                id = int(input("ID: "))
                name = input("New name: ")
                phone = input("New phone (leave blank to skip): ").strip() or None
                email = input("New email (leave blank to skip): ").strip() or None
                update_supplier(id, name, phone, email)
            case "4":
                list_suppliers()
                id = int(input("ID: "))
                delete_supplier(id)
            case "0":
                print("Going back...")
                break
            case _:
                print("Invalid option!")
