import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",  # change this
    database="hotel_db"
)
cursor = conn.cursor()

def book_room():
    name = input("Enter customer name: ")
    phone = input("Enter phone number: ")
    address = input("Enter address: ")
    check_in = input("Check-in date (YYYY-MM-DD): ")
    check_out = input("Check-out date (YYYY-MM-DD): ")

    cursor.execute("SELECT * FROM rooms WHERE status='available'")
    rooms = cursor.fetchall()

    if not rooms:
        print("No rooms available.")
        return

    print("Available rooms:")
    for room in rooms:
        print(f"Room No: {room[0]}, Type: {room[1]}, Price: {room[2]}")

    room_no = int(input("Enter room number to book: "))

    cursor.execute("UPDATE rooms SET status='booked' WHERE room_no=%s", (room_no,))
    cursor.execute("""
        INSERT INTO customers (name, phone, address, check_in, check_out, room_no)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, phone, address, check_in, check_out, room_no))
    
    conn.commit()
    print("Room booked successfully.")

def view_customers():
    cursor.execute("SELECT * FROM customers")
    for customer in cursor.fetchall():
        print(customer)

def check_room_availability():
    cursor.execute("SELECT * FROM rooms WHERE status='available'")
    for room in cursor.fetchall():
        print(f"Room No: {room[0]}, Type: {room[1]}, Price: {room[2]}")

def checkout():
    room_no = int(input("Enter room number for checkout: "))
    cursor.execute("SELECT price FROM rooms WHERE room_no=%s", (room_no,))
    price = cursor.fetchone()[0]

    cursor.execute("SELECT check_in, check_out FROM customers WHERE room_no=%s", (room_no,))
    data = cursor.fetchone()
    check_in = datetime.strptime(str(data[0]), "%Y-%m-%d")
    check_out = datetime.strptime(str(data[1]), "%Y-%m-%d")
    days = (check_out - check_in).days or 1

    total = days * price
    print(f"Total bill for room {room_no} is ₹{total:.2f} for {days} day(s)")

    cursor.execute("DELETE FROM customers WHERE room_no=%s", (room_no,))
    cursor.execute("UPDATE rooms SET status='available' WHERE room_no=%s", (room_no,))
    conn.commit()
    print("Checkout successful.")

def main():
    while True:
        print("\n---- Hotel Management ----")
        print("1. Book Room")
        print("2. View Customers")
        print("3. Check Room Availability")
        print("4. Checkout")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            book_room()
        elif choice == '2':
            view_customers()
        elif choice == '3':
            check_room_availability()
        elif choice == '4':
            checkout()
        elif choice == '5':
            break
        else:
            print("Invalid choice!")

main()
