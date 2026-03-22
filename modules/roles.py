import os
from modules.database import connect
from psycopg import errors


def create_role(name, base_salary):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = "INSERT INTO roles (name, base_salary) VALUES (%s, %s)"
                values = (name, base_salary)
                cur.execute(query, values)
        print(f"Role '{name}' created!")
    except Exception as e:
        print(f"Error: {e}")


def list_roles():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = "SELECT * FROM roles"
                cur.execute(query)
                roles = cur.fetchall()

                if not roles:
                    print("No roles found.")
                    return

                for role in roles:
                    role_id, name, base_salary = role
                    print(
                        f"""
ID: {role_id}
Name: {name}
Base Salary: {base_salary:.2f}
{'-' * 30}"""
                    )
    except Exception as e:
        print(f"Error: {e}")


def update_role(id, name, base_salary):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = "UPDATE roles SET name = %s, base_salary = %s WHERE id = %s"
                values = (name, base_salary, id)
                cur.execute(query, values)
        print("Role updated!")
    except Exception as e:
        print(f"Error: {e}")


def delete_role(id):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = "DELETE FROM roles WHERE id = %s"
                values = (id,)
                cur.execute(query, values)
        print("Role deleted!")
    except errors.ForeignKeyViolation:
        print("Error: role has employees — cannot delete!")
    except Exception as e:
        print(f"Error: {e}")


def menu_roles():
    while True:
        print("=== ROLES ===")
        print("1 - List roles")
        print("2 - Create role")
        print("3 - Update role")
        print("4 - Delete role")
        print("0 - Back")

        option = input("\nChoose: ")
        os.system("clear")

        match option:
            case "1":
                list_roles()
            case "2":
                name = input("Name: ")
                base_salary = float(input("Base salary: "))
                create_role(name, base_salary)
            case "3":
                list_roles()
                id = int(input("ID: "))
                name = input("New name: ")
                base_salary = float(input("New base salary: "))
                update_role(id, name, base_salary)
            case "4":
                list_roles()
                id = int(input("Role ID: "))
                delete_role(id)
            case "0":
                print("Going back...")
                break
            case _:
                print("Invalid option!")
