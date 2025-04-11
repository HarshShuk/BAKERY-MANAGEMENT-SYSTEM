import mysql.connector
from datetime import datetime

# Connect to MySQL database
try:
    con = mysql.connector.connect(host="localhost", user="root", password="root")
    cur = con.cursor()
except mysql.connector.Error as e:
    print(f"Error connecting to database: {e}")
    exit()

# Create and use the database
cur.execute("CREATE DATABASE IF NOT EXISTS Bakery_Management")
cur.execute("USE Bakery_Management")

# Create tables if not already present
cur.execute("""
    CREATE TABLE IF NOT EXISTS items (
        serial_No INT PRIMARY KEY,
        products VARCHAR(20),
        quantity INT,
        cost INT
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS flavours_cake (
        serial_No INT PRIMARY KEY,
        varieties VARCHAR(20),
        quantity INT,
        cost INT
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS workers (
        serial_No INT PRIMARY KEY,
        name VARCHAR(20),
        salary FLOAT
    )
""")

# Insert initial data if tables are empty
def initialize_data():
    cur.execute("SELECT * FROM items")
    if not cur.fetchall():
        cur.executemany("INSERT INTO items (serial_No, products, quantity, cost) VALUES (%s, %s, %s, %s)", [
            (1, 'Pastry', 40, 20),
            (2, 'Milk', 60, 60),
            (3, 'Butter', 30, 25),
            (4, 'Cheese', 25, 50),
            (5, 'Whole Wheat Bread', 25, 50)
        ])
        con.commit()

    cur.execute("SELECT * FROM flavours_cake")
    if not cur.fetchall():
        cur.executemany("INSERT INTO flavours_cake (serial_No, varieties, quantity, cost) VALUES (%s, %s, %s, %s)", [
            (1, 'Vanilla_Cake', 4,200),
            (2, 'Chocolate_Cake', 6,800),
            (3, 'Strawberry_Cake', 5,400),
            (4, 'Butter_scotch_Cake', 5,600)
        ])
        con.commit()

    cur.execute("SELECT * FROM workers")
    if not cur.fetchall():
        cur.executemany("INSERT INTO workers (serial_No, name, salary) VALUES (%s, %s, %s)", [
            (1, 'Mukesh', 2500.00),
            (2, 'Ram', 2000.00),
            (3, 'Suresh', 6000.00),
            (4, 'Raju', 2500.00),
            (5, 'Amit', 5000.00)
        ])
        con.commit()

initialize_data()

# Functions to display
def show_items():
    print("Items in the shop:")
    print(f"{'Serial No.':<25}{'Product':<35}{'Quantity':<20}{'Cost':<10}")
    print("-" * 85)
    cur.execute("SELECT * FROM items")
    items = cur.fetchall()
    for serial_no, product, quantity, cost in items:
        print(f"{serial_no:<25}{product:<35}{quantity:<20}{cost:<10}")

def show_worker_details():
    print("Workers in the shop:")
    cur.execute("SELECT * FROM workers")
    workers = cur.fetchall()
    for e_id, name, salary in workers:
        print(f"{e_id}:\t{name}:\tSalary: {salary}")

def show_flavours():
    print("\nCake flavours:")
    print(f"{'Serial No.':<15}{'Variety':<20}{'Quantity':<10}{'Cost':<10}")
    print("-" * 65)
    cur.execute("SELECT * FROM flavours_cake")
    for serial_no, variety, quantity, cost in cur.fetchall():
        print(f"{serial_no:<15}{variety:<20}{quantity:<10}{cost:<10}")

# Admin operations
def add_item(serial_no, product, quantity, cost):
    cur.execute("INSERT INTO items (serial_No, products, quantity, cost) VALUES (%s, %s, %s, %s)", (serial_no, product, quantity, cost))
    con.commit()
    print("Item added successfully.")

def update_quantity(serial_no, new_quantity):
    cur.execute("SELECT quantity FROM items WHERE serial_No = %s", (serial_no,))
    result = cur.fetchone()
    if result:
        current_quantity = result[0]
        cur.execute("UPDATE items SET quantity = %s WHERE serial_No = %s", (current_quantity + new_quantity, serial_no))
        con.commit()
        print("Quantity updated successfully.")
    else:
        print("Item not found.")

def update_cost(serial_no, new_cost):
    cur.execute("UPDATE items SET cost = %s WHERE serial_No = %s", (new_cost, serial_no))
    con.commit()
    print("Cost updated successfully.")

def add_cake_flavour(serial_no, varieties, quantity, cost):
    cur.execute("INSERT INTO flavours_cake (serial_No, varieties, quantity, cost) VALUES (%s, %s, %s, %s)", (serial_no, varieties, quantity, cost))
    con.commit()
    print("Flavour added successfully.")

def update_quantity_flavours(serial_no, new_quantity):
    cur.execute("UPDATE flavours_cake SET quantity = %s WHERE serial_No = %s", (new_quantity, serial_no))
    con.commit()
    print("Cake quantity updated successfully.")

def update_cost_flavours(serial_no, new_cost):
    cur.execute("UPDATE flavours_cake SET cost = %s WHERE serial_No = %s", (new_cost, serial_no))
    con.commit()
    print("Cake cost updated successfully.")

def delete_item(serial_no):
    cur.execute("SELECT * FROM items WHERE serial_No = %s", (serial_no,))
    if cur.fetchone():
        cur.execute("DELETE FROM items WHERE serial_No = %s", (serial_no,))
        con.commit()
        print(f"Item with Serial No. {serial_no} deleted successfully.")
    else:
        print(f"No item found with Serial No. {serial_no}.")
    show_items()

def remove_cake_flavour(serial_no):
    cur.execute("SELECT * FROM flavours_cake WHERE serial_No = %s", (serial_no,))
    if cur.fetchone():
        cur.execute("DELETE FROM flavours_cake WHERE serial_No = %s", (serial_no,))
        con.commit()
        print(f"Cake Flavour with Serial No. {serial_no} deleted successfully.")
    else:
        print(f"No cake flavour found with Serial No. {serial_no}.")
    show_flavours()

def add_worker(e_id, name, salary):
    cur.execute("INSERT INTO workers (serial_No, name, salary) VALUES (%s, %s, %s)", (e_id, name, salary))
    con.commit()
    print("Worker added successfully.")

def fire_worker(employee_id):
    cur.execute("SELECT * FROM workers WHERE serial_No = %s", (employee_id,))
    if cur.fetchone():
        cur.execute("DELETE FROM workers WHERE serial_No = %s", (employee_id,))
        con.commit()
        print(f"Worker with Employee ID {employee_id} has been removed from the system.")
    else:
        print(f"No worker found with Employee ID {employee_id}.")
    show_worker_details()


# Function to handle customer orders
def customer_order():
    orders = []
    name = input("Enter your name: ")
    phone = input("Enter your phone number: ")
    while True:
        print("\nWhat would you like to order?")
        print("1. Regular Items\n2. Cake Flavours\n3. Finish Order")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            show_items()
            serial_no = int(input("Enter the serial number of the item: "))
            cur.execute("SELECT * FROM items WHERE serial_No = %s", (serial_no,))
            item = cur.fetchone()
            if item:
                quantity = int(input("Enter the quantity: "))
                if quantity > item[2]:
                    print(f"Only {item[2]} available.")
                else:
                    total_cost = quantity * item[3]
                    orders.append([item[1], quantity, item[3], total_cost])
                    cur.execute("UPDATE items SET quantity = quantity - %s WHERE serial_No = %s", (quantity, serial_no))
                    con.commit()
                    print(f"Added {quantity} {item[1]}(s) to your order.")
            else:
                print("Item not found.")
        elif choice == 2:
            show_flavours()
            serial_no = int(input("Enter the serial number of the cake flavour: "))
            cur.execute("SELECT * FROM flavours_cake WHERE serial_No = %s", (serial_no,))
            cake = cur.fetchone()
            if cake:
                quantity = int(input("Enter the quantity: "))
                if quantity > cake[2]:
                    print(f"Only {cake[2]} available.")
                else:
                    total_cost = quantity * cake[3]
                    orders.append([cake[1], quantity, cake[3], total_cost])
                    cur.execute("UPDATE flavours_cake SET quantity = quantity - %s WHERE serial_No = %s", (quantity, serial_no))
                    con.commit()
                    print(f"Added {quantity} {cake[1]} cake(s) to your order.")
            else:
                print("Cake flavour not found.")
        elif choice == 3:
            print("Finalizing your order...")
            break
        else:
            print("Invalid choice.")
    
    if orders:
        # Generate and display the bill
        print("\n===== BILL =====")
        print(f"Customer Name: {name}")
        print(f"Phone Number: {phone}")
        print("\nItems Ordered:")
        print(f"{'Item':<20}{'Quantity':<10}{'Cost per Unit':<15}{'Total Cost':<10}")
        print("-" * 65)
        total_amount = 0
        for item, qty, cost_per_unit, total_cost in orders:
            print(f"{item:<20}{qty:<10}{cost_per_unit:<15}{total_cost:<10}")
            total_amount += total_cost
        print("\nTotal Amount:", total_amount)
        print("================\n")

        # Save the bill to a file
        file_name = f"{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_bill.txt"
        with open(file_name, "w") as file:
            file.write("===== BILL =====\n")
            file.write(f"Customer Name: {name}\n")
            file.write(f"Phone Number: {phone}\n\n")
            file.write("Items Ordered:\n")
            file.write(f"{'Item':<20}{'Quantity':<10}{'Cost per Unit':<15}{'Total Cost':<10}\n")
            file.write("-" * 65)
            for item, qty, cost_per_unit, total_cost in orders:
                file.write(f"\n{item:<20}{qty:<10}{cost_per_unit:<15}{total_cost:<10}")
            file.write(f"\n\nTotal Amount: {total_amount}\n")
            file.write("================\n")
        print(f"Bill saved as {file_name}.")
    else:
        print("No orders placed.")


# Main Program
print("______________________________##Class 12th CS PROJECT(083)##_______________________________")
print("___________________________________________________________________________________________")
print("| ............................. @@@@@@@@@ WELCOME @@@@@@@@@ ............................. |")
print("| .............................   BAKERY MANAGEMENT SYSTEM  ............................. |")
print("| .............................          MADE BY:           ............................. |")
print("| ........................ #HARSH#, #BAIBHAV#, #ANUJ#, #AVINASH# ........................ |")
print("| .........................  SUBMITTED TO: R.P. KUSHWAHA SIR    ......................... |")
print("| ..........................          SESSION: 2024-2025       .......................... |")
print("___________________________________________________________________________________________")

while True:
    try:
        print("\nPlease choose:\n1. For Admin\n2. For Customer\n3. For Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            admin_name = input("Username: ")
            if admin_name.lower() in ['anuj', 'harsh', 'baibhav', 'avinash']:
                passkey = int(input("Enter Password: "))
                passwords = {'anuj': 8318, 'harsh': 9555, 'baibhav': 9919, 'avinash': 9511}
                if passwords.get(admin_name.lower()) == passkey:
                    print(f"Welcome, {admin_name.title()}!")
                    print("""01: Add item\n02: View items
03: Add cake flavour\n04: View cake flavours
05: Update Quantity of cake flavour\n06: Update cost of cake flavour
07: Update Quantity\n08: Update item cost
09: Delete item\n10: Delete cake flavour
11: Add worker\n12: Fire worker""")
                    admin_choice = int(input("Enter your choice: "))
                    if admin_choice == 1:
                        print("Current item:")
                        show_items()
                        add_item(int(input("Serial No: ")), input("Product: "), int(input("Quantity: ")), int(input("Cost: ")))
                    elif admin_choice == 2:
                        show_items()
                    elif admin_choice == 3:
                        print("Current Flavours:")
                        show_flavours()
                        add_cake_flavour(int(input("Serial No: ")), input("Variety: "), int(input("Quantity: ")), int(input("Cost: ")))
                    elif admin_choice == 4:
                        show_flavours()
                    elif admin_choice == 5:
                        update_quantity_flavours(int(input("Serial No: ")), int(input("New Quantity: ")))
                    elif admin_choice == 6:
                        update_cost_flavours(int(input("Serial No: ")), int(input("New Cost: ")))        
                    elif admin_choice == 7:
                        update_quantity(int(input("Serial No: ")), int(input("New Quantity: ")))
                    elif admin_choice == 8:
                        update_cost(int(input("Serial No: ")), int(input("New Cost: ")))
                    elif admin_choice == 9:
                        print("Current item:")
                        show_items()
                        delete_item(int(input("Serial No: ")))
                    elif admin_choice == 10:
                        print("Current Flavours:")
                        show_flavours()
                        remove_cake_flavour(int(input("Serial No: ")))
                    elif admin_choice == 11:
                        add_worker(int(input("Employee ID: ")), input("Name: "), float(input("Salary: ")))
                    elif admin_choice == 12:
                        fire_worker(int(input("Employee ID: ")))
                    else:
                        print("Invalid choice.")
                else:
                    print("Incorrect password.")
            else:
                print("Access denied.")
        elif choice == 2:
            customer_order()
        elif choice == 3:
            print("Thanks for visiting!")
            break
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

con.close()