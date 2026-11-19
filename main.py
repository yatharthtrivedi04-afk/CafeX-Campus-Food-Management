# CafeX - Campus Food Ordering and Outlet Management System
# Runs with Python 3 and uses only built-in libraries.

import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CAFE_FILE = DATA_DIR / "cafes.csv"
MENU_FILE = DATA_DIR / "menu.csv"
USER_FILE = DATA_DIR / "users.csv"
ORDER_FILE = DATA_DIR / "orders.csv"
BOOKING_FILE = DATA_DIR / "bookings.csv"

CAFE_HEADERS = ["cafe_id", "name", "opening", "closing", "status", "account_status", "seats"]
MENU_HEADERS = ["cafe_id", "item", "category", "price", "stock", "available"]
USER_HEADERS = ["username", "password", "role", "cafe_id"]
ORDER_HEADERS = ["order_id", "customer", "cafe", "item", "quantity", "total", "order_type", "status", "time"]
BOOKING_HEADERS = ["booking_id", "customer", "cafe", "people", "time", "status"]


INITIAL_CAFES = [
    ["CAFE-001", "GreenOx", "08:00", "22:00", "Open", "Active", "40"],
    ["CAFE-002", "Subway", "09:00", "22:00", "Open", "Active", "50"],
    ["CAFE-003", "Domino's", "10:00", "23:00", "Open", "Active", "35"],
    ["CAFE-004", "Southern Stories", "08:00", "22:00", "Open", "Active", "60"],
]
INITIAL_USERS = [
    ["fbmanager", "fbmanager123", "fnb_manager", ""],
    ["greenox", "greenox123", "outlet_manager", "CAFE-001"],
    ["subway", "subway123", "outlet_manager", "CAFE-002"],
    ["dominos", "dominos123", "outlet_manager", "CAFE-003"],
    ["southern", "southern123", "outlet_manager", "CAFE-004"],
]
INITIAL_MENU = [
    ["CAFE-001", "Classic Veg Sandwich", "Snacks", "119", "20", "Yes"],
    ["CAFE-001", "Paneer Protein Bowl", "Meals", "189", "15", "Yes"],
    ["CAFE-001", "Mexican Veg Wrap", "Snacks", "149", "18", "Yes"],
    ["CAFE-001", "Fresh Fruit Bowl", "Healthy", "129", "12", "Yes"],
    ["CAFE-001", "Cold Coffee", "Drinks", "99", "25", "Yes"],
    ["CAFE-001", "Veggie Salad", "Healthy", "139", "12", "Yes"],
    ["CAFE-001", "Grilled Paneer Sandwich", "Snacks", "159", "15", "Yes"],
    ["CAFE-001", "Lemon Iced Tea", "Drinks", "79", "20", "Yes"],
    ["CAFE-002", "Veggie Delight Sub", "Subs", "159", "20", "Yes"],
    ["CAFE-002", "Paneer Tikka Sub", "Subs", "199", "15", "Yes"],
    ["CAFE-002", "Aloo Patty Sub", "Subs", "149", "18", "Yes"],
    ["CAFE-002", "Chicken Teriyaki Sub", "Subs", "229", "12", "Yes"],
    ["CAFE-002", "Choco Chip Cookie", "Desserts", "49", "30", "Yes"],
    ["CAFE-002", "Corn and Peas Sub", "Subs", "179", "15", "Yes"],
    ["CAFE-002", "Veg Seekh Sub", "Subs", "189", "12", "Yes"],
    ["CAFE-002", "Cold Coffee", "Drinks", "99", "20", "Yes"],
    ["CAFE-003", "Margherita Pizza", "Pizza", "99", "20", "Yes"],
    ["CAFE-003", "Farmhouse Pizza", "Pizza", "249", "15", "Yes"],
    ["CAFE-003", "Peppy Paneer Pizza", "Pizza", "229", "15", "Yes"],
    ["CAFE-003", "Garlic Breadsticks", "Sides", "109", "20", "Yes"],
    ["CAFE-003", "Choco Lava Cake", "Desserts", "109", "18", "Yes"],
    ["CAFE-003", "Veg Extravaganza", "Pizza", "299", "10", "Yes"],
    ["CAFE-003", "Cheese Burst Pizza", "Pizza", "279", "12", "Yes"],
    ["CAFE-003", "Stuffed Garlic Bread", "Sides", "149", "15", "Yes"],
    ["CAFE-004", "Plain Masala Dosa", "South Indian", "119", "20", "Yes"],
    ["CAFE-004", "Mysore Masala Dosa", "South Indian", "149", "15", "Yes"],
    ["CAFE-004", "Idli Sambhar (2 pcs)", "South Indian", "69", "25", "Yes"],
    ["CAFE-004", "Medu Vada (2 pcs)", "South Indian", "79", "20", "Yes"],
    ["CAFE-004", "Onion Uttapam", "South Indian", "129", "15", "Yes"],
    ["CAFE-004", "Podi Idli", "South Indian", "99", "15", "Yes"],
    ["CAFE-004", "Rava Dosa", "South Indian", "139", "12", "Yes"],
    ["CAFE-004", "Filter Coffee", "Drinks", "59", "25", "Yes"],
]

def ensure_csv(path, headers, rows):
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

def setup_files():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ensure_csv(CAFE_FILE, CAFE_HEADERS, INITIAL_CAFES)
    ensure_csv(MENU_FILE, MENU_HEADERS, INITIAL_MENU)
    ensure_csv(USER_FILE, USER_HEADERS, INITIAL_USERS)
    ensure_csv(ORDER_FILE, ORDER_HEADERS, [])
    ensure_csv(BOOKING_FILE, BOOKING_HEADERS, [])

def read_csv(path):
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path, headers, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

def add_csv(path, row):
    with path.open("a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)

def title(text):
    print("\n" + "=" * 58)
    print(text.center(58))
    print("=" * 58)

def pause():
    input("\nPress Enter to continue...")

def get_cafe_id(name):
    for cafe in read_csv(CAFE_FILE):
        if cafe["name"].lower() == name.lower():
            return cafe
    return None

def get_cafe_by_id(cafe_id):
    for cafe in read_csv(CAFE_FILE):
        if cafe["cafe_id"] == cafe_id:
            return cafe
    return None

def show_cafes(include_inactive=False):
    cafes = read_csv(CAFE_FILE)
    print("\n{:<4} {:<20} {:<13} {:<24}".format("No", "Outlet", "Timings", "Status"))
    print("-" * 64)
    shown = 0
    for cafe in cafes:
        if include_inactive or cafe["account_status"] == "Active":
            shown += 1
            print("{:<4} {:<20} {:<13} {:<24}".format(
                shown, cafe["name"], cafe["opening"] + "-" + cafe["closing"],
                cafe["status"] + " / " + cafe["account_status"]))
    if not shown:
        print("No outlets available.")

def show_menu(cafe_id):
    print("\n{:<4} {:<28} {:<15} {:>8} {:>7}".format("No", "Item", "Category", "Price", "Stock"))
    print("-" * 68)
    count = 0
    for item in read_csv(MENU_FILE):
        if item["cafe_id"] == cafe_id:
            count += 1
            print("{:<4} {:<28} {:<15} {:>8} {:>7}".format(
                count, item["item"][:27], item["category"][:14], "Rs." + item["price"], item["stock"]))
    if count == 0:
        print("No menu items.")

def login():
    title("CAFEX LOGIN")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    for user in read_csv(USER_FILE):
        if user["username"] == username and user["password"] == password:
            print("Login successful. Welcome", username)
            return user
    print("Wrong username or password.")
    pause()
    return None

def register_customer():
    title("CREATE CUSTOMER ACCOUNT")
    username = input("Choose username: ").strip()
    password = input("Choose password: ").strip()
    if not username or not password:
        print("Username/password cannot be empty.")
        pause()
        return
    for user in read_csv(USER_FILE):
        if user["username"].lower() == username.lower():
            print("Username already exists.")
            pause()
            return
    add_csv(USER_FILE, [username, password, "customer", ""])
    print("Account created. You can now log in.")
    pause()

def fnb_manager_menu(user):
    while True:
        title("CAMPUS F&B MANAGER")
        print("1. View outlets\n2. Update outlet timings\n3. Update outlet status")
        print("4. View all orders\n5. View all reservations\n6. Logout")
        choice = input("Choice: ").strip()
        if choice == "1":
            show_cafes(True); pause()
        elif choice == "2":
            show_cafes(True)
            cafe = get_cafe_id(input("Outlet name: ").strip())
            if not cafe:
                print("Outlet not found.")
            else:
                opening = input("Opening time (HH:MM): ").strip()
                closing = input("Closing time (HH:MM): ").strip()
                try:
                    datetime.strptime(opening, "%H:%M"); datetime.strptime(closing, "%H:%M")
                    cafes = read_csv(CAFE_FILE)
                    for row in cafes:
                        if row["cafe_id"] == cafe["cafe_id"]:
                            row["opening"], row["closing"] = opening, closing
                    write_csv(CAFE_FILE, CAFE_HEADERS, cafes)
                    print("Timings updated.")
                except ValueError:
                    print("Invalid time format.")
            pause()
        elif choice == "3":
            show_cafes(True)
            cafe = get_cafe_id(input("Outlet name: ").strip())
            if not cafe:
                print("Outlet not found.")
            else:
                daily = input("Daily status (1 Open, 2 Closed, 3 Temporarily Closed): ").strip()
                account = input("Account status (1 Active, 2 Suspended, 3 Terminated): ").strip()
                dmap = {"1": "Open", "2": "Closed", "3": "Temporarily Closed"}
                amap = {"1": "Active", "2": "Suspended", "3": "Terminated"}
                if daily in dmap and account in amap:
                    cafes = read_csv(CAFE_FILE)
                    for row in cafes:
                        if row["cafe_id"] == cafe["cafe_id"]:
                            row["status"], row["account_status"] = dmap[daily], amap[account]
                    write_csv(CAFE_FILE, CAFE_HEADERS, cafes)
                    print("Status updated.")
                else:
                    print("Invalid selection.")
            pause()
        elif choice == "4":
            title("ALL ORDERS")
            orders = read_csv(ORDER_FILE)
            if not orders: print("No orders yet.")
            for o in orders:
                print(o["order_id"], "|", o["customer"], "|", o["cafe"], "|", o["item"], "| Qty:", o["quantity"], "| Rs.", o["total"], "|", o["status"])
            pause()
        elif choice == "5":
            title("ALL RESERVATIONS")
            bookings = read_csv(BOOKING_FILE)
            if not bookings: print("No reservations yet.")
            for b in bookings:
                print(b["booking_id"], "|", b["customer"], "|", b["cafe"], "| People:", b["people"], "|", b["time"], "|", b["status"])
            pause()
        elif choice == "6":
            return
        else:
            print("Invalid choice."); pause()

def outlet_manager_menu(user):
    cafe_id = user["cafe_id"]
    cafe = get_cafe_by_id(cafe_id)
    cafe_name = cafe["name"] if cafe else "Outlet"
    while True:
        title(cafe_name.upper() + " - OUTLET MANAGER")
        print("1. View menu/stock\n2. Add menu item\n3. Update stock\n4. View incoming orders")
        print("5. Complete an order\n6. View reservations\n7. Logout")
        choice = input("Choice: ").strip()
        if choice == "1":
            show_menu(cafe_id); pause()
        elif choice == "2":
            name = input("Item name: ").strip(); category = input("Category: ").strip()
            price = input("Price (rupees): ").strip(); stock = input("Stock: ").strip()
            if name and category and price.isdigit() and stock.isdigit():
                add_csv(MENU_FILE, [cafe_id, name, category, price, stock, "Yes" if int(stock) else "No"])
                print("Item added.")
            else: print("Enter a name/category and numeric price/stock.")
            pause()
        elif choice == "3":
            show_menu(cafe_id)
            name = input("Exact item name: ").strip(); stock = input("New stock: ").strip()
            if not stock.isdigit(): print("Stock must be a whole number.")
            else:
                items = read_csv(MENU_FILE); found = False
                for item in items:
                    if item["cafe_id"] == cafe_id and item["item"].lower() == name.lower():
                        item["stock"] = stock; item["available"] = "Yes" if int(stock) else "No"; found = True
                if found: write_csv(MENU_FILE, MENU_HEADERS, items); print("Stock updated.")
                else: print("Item not found.")
            pause()
        elif choice == "4":
            title("OUTLET ORDERS"); found = False
            for order in read_csv(ORDER_FILE):
                if order["cafe"] == cafe_name:
                    found = True
                    print(order["order_id"], "|", order["customer"], "|", order["item"], "| Qty:", order["quantity"], "| Rs.", order["total"], "|", order["status"])
            if not found: print("No orders for this outlet.")
            pause()
        elif choice == "5":
            order_id = input("Order ID: ").strip(); orders = read_csv(ORDER_FILE); found = False
            for order in orders:
                if order["order_id"] == order_id and order["cafe"] == cafe_name:
                    order["status"] = "Completed"; found = True
            if found: write_csv(ORDER_FILE, ORDER_HEADERS, orders); print("Order completed.")
            else: print("Order not found for your outlet.")
            pause()
        elif choice == "6":
            found = False
            for booking in read_csv(BOOKING_FILE):
                if booking["cafe"] == cafe_name:
                    found = True
                    print(booking["booking_id"], "|", booking["customer"], "| People:", booking["people"], "|", booking["time"], "|", booking["status"])
            if not found: print("No reservations for this outlet.")
            pause()
        elif choice == "7": return
        else: print("Invalid choice."); pause()

def customer_menu(user):
    while True:
        title("CUSTOMER DASHBOARD")
        print("1. Browse outlets\n2. View outlet menu\n3. Place order\n4. Reserve seats\n5. View my activity\n6. Logout")
        choice = input("Choice: ").strip()
        if choice == "1": show_cafes(); pause()
        elif choice == "2":
            show_cafes(); cafe = get_cafe_id(input("Outlet name: ").strip())
            if cafe and cafe["account_status"] == "Active": show_menu(cafe["cafe_id"])
            else: print("Outlet unavailable.")
            pause()
        elif choice == "3": place_order(user); pause()
        elif choice == "4": reserve_seats(user); pause()
        elif choice == "5": customer_activity(user); pause()
        elif choice == "6": return
        else: print("Invalid choice."); pause()

def place_order(user):
    show_cafes(); cafe = get_cafe_id(input("Outlet name: ").strip())
    if not cafe or cafe["status"] != "Open" or cafe["account_status"] != "Active":
        print("Outlet is not accepting orders."); return
    show_menu(cafe["cafe_id"])
    name = input("Exact item name: ").strip(); qty_text = input("Quantity: ").strip()
    if not qty_text.isdigit() or int(qty_text) < 1: print("Invalid quantity."); return
    qty = int(qty_text); items = read_csv(MENU_FILE); selected = None
    for item in items:
        if item["cafe_id"] == cafe["cafe_id"] and item["item"].lower() == name.lower(): selected = item
    if not selected or selected["available"] != "Yes": print("Item unavailable."); return
    if int(selected["stock"]) < qty: print("Not enough stock."); return
    typ = input("Order type (1 Takeaway / 2 Dine-in): ").strip()
    if typ not in ("1", "2"): print("Invalid type."); return
    total = int(selected["price"]) * qty
    orders = read_csv(ORDER_FILE); order_id = "ORD-" + str(len(orders) + 1).zfill(4)
    add_csv(ORDER_FILE, [order_id, user["username"], cafe["name"], selected["item"], qty, total, "Takeaway" if typ == "1" else "Dine-in", "Placed", datetime.now().strftime("%d-%m-%Y %H:%M")])
    for item in items:
        if item["cafe_id"] == cafe["cafe_id"] and item["item"] == selected["item"]:
            item["stock"] = str(int(item["stock"]) - qty)
            item["available"] = "Yes" if int(item["stock"]) > 0 else "No"
    write_csv(MENU_FILE, MENU_HEADERS, items)
    print("Order placed! ID:", order_id, "Total: Rs.", total)

def reserve_seats(user):
    show_cafes(); cafe = get_cafe_id(input("Outlet name: ").strip())
    if not cafe or cafe["status"] != "Open" or cafe["account_status"] != "Active":
        print("Outlet is not accepting reservations."); return
    people = input("Number of people: ").strip(); time_text = input("Preferred time (HH:MM): ").strip()
    if not people.isdigit() or int(people) < 1: print("Invalid number of people."); return
    try: datetime.strptime(time_text, "%H:%M")
    except ValueError: print("Time must be HH:MM."); return
    bookings = read_csv(BOOKING_FILE); booking_id = "BOOK-" + str(len(bookings) + 1).zfill(4)
    add_csv(BOOKING_FILE, [booking_id, user["username"], cafe["name"], people, time_text, "Requested"])
    print("Reservation request saved. ID:", booking_id)

def customer_activity(user):
    print("\nMY ORDERS"); found = False
    for order in read_csv(ORDER_FILE):
        if order["customer"] == user["username"]:
            found = True
            print(order["order_id"], "|", order["cafe"], "|", order["item"], "| Qty:", order["quantity"], "| Rs.", order["total"], "|", order["status"])
    if not found: print("No orders yet.")
    print("\nMY RESERVATIONS"); found = False
    for booking in read_csv(BOOKING_FILE):
        if booking["customer"] == user["username"]:
            found = True
            print(booking["booking_id"], "|", booking["cafe"], "| People:", booking["people"], "|", booking["time"], "|", booking["status"])
    if not found: print("No reservations yet.")

def main():
    setup_files()
    while True:
        title("CAFEX - CAMPUS FOOD MANAGEMENT")
        print("1. Login\n2. Create customer account\n3. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            user = login()
            if user:
                if user["role"] == "fnb_manager": fnb_manager_menu(user)
                elif user["role"] == "outlet_manager": outlet_manager_menu(user)
                elif user["role"] == "customer": customer_menu(user)
        elif choice == "2": register_customer()
        elif choice == "3": print("Thanks for using CafeX!"); break
        else: print("Choose 1, 2 or 3."); pause()

if __name__ == "__main__":
    main()
