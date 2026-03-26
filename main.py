import os
from modules.categories import menu_categories
from modules.suppliers import menu_suppliers
from modules.roles import menu_roles
from modules.products import menu_products
from modules.customers import menu_customers
from modules.employees import menu_employees
from modules.sales import menu_sales


def main():
    while True:
        print("\n=== SUPERMARKET SYSTEM ===")
        print("1 - Categories")
        print("2 - Suppliers")
        print("3 - Roles")
        print("4 - Products")
        print("5 - Customers")
        print("6 - Employees")
        print("7 - Sales")
        print("0 - Exit")

        option = input("\nChoose: ")
        os.system("clear")

        match option:
            case "1":
                menu_categories()
            case "2":
                menu_suppliers()
            case "3":
                menu_roles()
            case "4":
                menu_products()
            case "5":
                menu_customers()
            case "6":
                menu_employees()
            case "7":
                menu_sales()
            case "0":
                print("Goodbye!")
                break
            case _:
                print("Invalid option!")


if __name__ == "__main__":
    main()