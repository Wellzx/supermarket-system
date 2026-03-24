import os
from modules.database import connect
from modules.categories import list_categories
from modules.suppliers import list_suppliers
from psycopg import errors


def create_product(name, price, stock, category_id, supplier_id):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = """
                INSERT INTO products (name, price, stock, category_id, supplier_id)
                VALUES (%s, %s, %s, %s, %s)
                """
                values = (name, price, stock, category_id, supplier_id)
                cur.execute(query, values)
        print(f"Product '{name}' created!")
    except errors.ForeignKeyViolation:
        print("Error: category or supplier not found!")
    except Exception as e:
        print(f"Error: {e}")


def list_products():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = """
                SELECT
                p.id,
                p.name,
                p.price,
                p.stock,
                c.name AS category,
                s.name AS supplier
                FROM products p
                JOIN categories c ON p.category_id = c.id
                JOIN suppliers s ON p.supplier_id = s.id
                ORDER BY p.name
                """
                cur.execute(query)
                products = cur.fetchall()

                if not products:
                    print("No product found!")
                    return

                print("\n=== Products ===")
                for product in products:
                    product_id, name, price, stock, category, supplier = product
                    print(
                        f"""
ID: {product_id}
Name: {name}
Price: R${price:.2f}
Stock: {stock}
Category: {category}
Supplier: {supplier}
{'-' * 30}"""
                    )
    except Exception as e:
        print(f"Error: {e}")


def update_product(id, name, price, stock, category_id, supplier_id):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = """
                UPDATE products
                SET name = %s, price = %s, stock = %s, category_id = %s, supplier_id = %s
                WHERE id = %s
                """
                values = (name, price, stock, category_id, supplier_id, id)
                cur.execute(query, values)
        print("Product updated!")
    except errors.ForeignKeyViolation:
        print("Error: category or supplier not found!")
    except Exception as e:
        print(f"Error: {e}")


def delete_product(id):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = "DELETE FROM products WHERE id = %s"
                values = (id,)
                cur.execute(query, values)
        print("Product deleted!")
    except errors.ForeignKeyViolation:
        print("Error: product has sales registered - cannot delete!")
    except Exception as e:
        print(f"Error: {e}")


def menu_products():
    while True:
        print("\n=== PRODUCTS ===")
        print("1 - List products")
        print("2 - Create product")
        print("3 - Update product")
        print("4 - Delete product")
        print("0 - Back")

        option = input("\nChoose: ")
        os.system("clear")

        match option:
            case "1":
                list_products()
            case "2":
                list_categories()
                list_suppliers()
                name = input("Name: ")
                price = float(input("Price: "))
                stock = int(input("Stock: "))
                category_id = int(input("Category ID: "))
                supplier_id = int(input("Supplier ID: "))
                create_product(name, price, stock, category_id, supplier_id)
            case "3":
                list_products()
                id = int(input("ID: "))
                list_categories()
                list_suppliers()
                name = input("New name: ")
                price = float(input("New price: "))
                stock = int(input("New stock: "))
                category_id = int(input("New category ID: "))
                supplier_id = int(input("New supplier ID: "))
                update_product(id, name, price, stock, category_id, supplier_id)
            case "4":
                list_products()
                id = int(input("ID: "))
                delete_product(id)
            case "0":
                print("Going back...")
                break
            case _:
                print("Invalid option!")
