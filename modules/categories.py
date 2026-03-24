import os
from modules.database import connect
from psycopg import errors


def create_category(name):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = "INSERT INTO categories (name) VALUES (%s)"
                values = (name,)
                cur.execute(query, values)
        print(f"Category '{name}' created!")
    except Exception as e:
        print(f"Error: {e}")


def list_categories():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = "SELECT * FROM categories"
                cur.execute(query)
                categories = cur.fetchall()

                if not categories:
                    print("No categories found.")
                    return
                
                print("\n=== Categories ===")
                for category in categories:
                    category_id, name = category
                    print(
                        f"""
ID: {category_id}
Name: {name}
{'-' * 30}"""
                    )

    except Exception as e:
        print(f"Error: {e}")


def update_category(id, name):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = "UPDATE categories SET name = %s WHERE id = %s"
                values = (name, id)
                cur.execute(query, values)
        print("Category updated!")
    except Exception as e:
        print(f"Error: {e}")


def delete_category(id):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = "DELETE FROM categories WHERE id = %s"
                values = (id,)
                cur.execute(query, values)
        print("Category deleted!")
    except errors.ForeignKeyViolation:
        print("Error: category has products — cannot delete!")
    except Exception as e:
        print(f"Error: {e}")


def menu_categories():
    while True:
        print("=== CATEGORIES ===")
        print("1 - List categories")
        print("2 - Create category")
        print("3 - Update category")
        print("4 - Delete category")
        print("0 - Back")

        option = input("\nChoose: ")
        os.system("clear")

        match option:
            case "1":
                list_categories()
            case "2":
                name = input("Name: ")
                create_category(name)
            case "3":
                list_categories()
                id = int(input("ID: "))
                name = input("New name: ")
                update_category(id, name)
            case "4":
                list_categories()
                id = int(input("Category ID: "))
                delete_category(id)
            case "0":
                print("Going back...")
                break
            case _:
                print("Invalid option!")
