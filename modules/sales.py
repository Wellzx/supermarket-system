import os
from modules.database import connect
from modules.products import list_products
from modules.customers import list_customers
from modules.employees import list_employees
from psycopg import errors


def create_sale(customer_id, employee_id, items):
    try:
        with connect() as conn:
            with conn.cursor() as cur:

                for product_id, quantity, unit_price in items:
                    cur.execute(
                        "SELECT stock, name FROM products WHERE id = %s",
                        (product_id,)
                    )
                    product = cur.fetchone()

                    if not product:
                        print(f"Product ID {product_id} not found!")
                        return

                    stock, name = product
                    if stock < quantity:
                        print(f"Insufficient stock for '{name}'. Available: {stock}")
                        return

                total = sum(qty * price for _, qty, price in items)

                query = """
                    INSERT INTO sales (customer_id, employee_id, total)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """
                values = (customer_id, employee_id, total)
                cur.execute(query, values)
                sale_id = cur.fetchone()[0]

                for product_id, quantity, unit_price in items:
                    cur.execute(
                        """
                        INSERT INTO sale_items (sale_id, product_id, quantity, unit_price)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (sale_id, product_id, quantity, unit_price)
                    )
                    cur.execute(
                        "UPDATE products SET stock = stock - %s WHERE id = %s",
                        (quantity, product_id)
                    )

        print(f"""
Sale registered successfully!
Sale ID: {sale_id}
Total: R${total:.2f}
{'-' * 30}""")

    except errors.ForeignKeyViolation:
        print("Error: customer or employee not found!")
    except Exception as e:
        print(f"Error: {e}")


def list_sales():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT
                        s.id,
                        s.date,
                        s.total,
                        c.name AS customer,
                        e.name AS employee
                    FROM sales s
                    LEFT JOIN customers c ON s.customer_id = c.id
                    JOIN employees e ON s.employee_id = e.id
                    ORDER BY s.date DESC
                """
                cur.execute(query)
                sales = cur.fetchall()

                if not sales:
                    print("No sales found.")
                    return

                print("\n=== SALES ===")
                for sale in sales:
                    sale_id, date, total, customer, employee = sale
                    print(f"""
ID: {sale_id}
Date: {date.strftime('%d/%m/%Y %H:%M')}
Total: R${total:.2f}
Customer: {customer or 'Anonymous'}
Employee: {employee}
{'-' * 30}""")

    except Exception as e:
        print(f"Error: {e}")


def list_sale_items(sale_id):
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT
                        p.name,
                        si.quantity,
                        si.unit_price,
                        si.quantity * si.unit_price AS subtotal
                    FROM sale_items si
                    JOIN products p ON si.product_id = p.id
                    WHERE si.sale_id = %s
                """
                cur.execute(query, (sale_id,))
                items = cur.fetchall()

                if not items:
                    print("No items found for this sale.")
                    return

                print(f"\n=== ITEMS — SALE #{sale_id} ===")
                for item in items:
                    name, quantity, unit_price, subtotal = item
                    print(f"""
Product: {name}
Quantity: {quantity}
Unit price: R${unit_price:.2f}
Subtotal: R${subtotal:.2f}
{'-' * 30}""")

    except Exception as e:
        print(f"Error: {e}")


def delete_sale(sale_id):
    try:
        with connect() as conn:
            with conn.cursor() as cur:

                cur.execute(
                    "SELECT product_id, quantity FROM sale_items WHERE sale_id = %s",
                    (sale_id,)
                )
                items = cur.fetchall()

                for product_id, quantity in items:
                    cur.execute(
                        "UPDATE products SET stock = stock + %s WHERE id = %s",
                        (quantity, product_id)
                    )

                cur.execute(
                    "DELETE FROM sale_items WHERE sale_id = %s",
                    (sale_id,)
                )

                cur.execute(
                    "DELETE FROM sales WHERE id = %s",
                    (sale_id,)
                )

        print(f"Sale #{sale_id} deleted and stock restored!")

    except Exception as e:
        print(f"Error: {e}")


def menu_sales():
    while True:
        print("\n=== SALES ===")
        print("1 - List sales")
        print("2 - New sale")
        print("3 - View sale items")
        print("4 - Delete sale")
        print("0 - Back")

        option = input("\nChoose: ")
        os.system("clear")

        match option:
            case "1":
                list_sales()

            case "2":
                list_customers()
                customer_input = input("\nCustomer ID (leave blank for anonymous): ").strip()
                customer_id = int(customer_input) if customer_input else None

                list_employees()
                employee_id = int(input("\nEmployee ID: "))

                items = []
                print("\nAdd products (leave blank to finish):")

                while True:
                    list_products()
                    product_input = input("\nProduct ID (leave blank to finish): ").strip()
                    if not product_input:
                        break

                    product_id = int(product_input)
                    quantity = int(input("Quantity: "))

                    try:
                        with connect() as conn:
                            with conn.cursor() as cur:
                                cur.execute(
                                    "SELECT price, name FROM products WHERE id = %s",
                                    (product_id,)
                                )
                                result = cur.fetchone()
                                if result:
                                    unit_price, name = result
                                    print(f"  {name} — R${unit_price:.2f} each")
                                    items.append((product_id, quantity, unit_price))
                                else:
                                    print("Product not found!")
                    except Exception as e:
                        print(f"Error: {e}")

                if not items:
                    print("No items added. Sale cancelled.")
                else:
                    create_sale(customer_id, employee_id, items)

            case "3":
                list_sales()
                sale_id = int(input("\nSale ID: "))
                list_sale_items(sale_id)

            case "4":
                list_sales()
                sale_id = int(input("\nSale ID: "))
                delete_sale(sale_id)

            case "0":
                print("Going back...")
                break

            case _:
                print("Invalid option!")