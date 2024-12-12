from datetime import datetime
from reservation import Reservations
from orderingSystem import OrderingSystem
from stats import Stats

class UserInterface:
    def __init__(self, database):
        self.database = database
        self.report = Stats(database)
        self.ordering_system = OrderingSystem(database)
        self.reservation_system = Reservations(database)

    #order section of userInterface class
    def display_menu(self):
        print("Menu: 1. Pizza ($25), 2. Burger ($30), 3. Salad ($15)")

    def receive_order(self):
        customer_name = input("Enter customer name: ")
        items = []
        while True:
            item_choice = input("Enter item number (1-3), 'edit' to change item/quantity or 'done' to finish: ")
            if item_choice.lower() == 'done':
                break
            elif item_choice.lower() == 'edit':
                item_id = input("Enter item_id of item to change (001, 002, 003): ")
                found = False
                for item in items:
                    if item['item_id'] == item_id:
                        quantity = int(input(f"Enter new quantity for {item['name']}: "))
                        item['quantity'] = quantity
                        item['total_price'] = quantity * item['unit_price']
                        print(f"Updated {item['name']} to quantity {quantity}.")
                        found = True
                        break
                if not found:
                    print(f"Item of item_id {item_id} not found in the order.")
                continue
            
            item_quantity = int(input("Enter quantity: "))
            match item_choice:
                case '1':
                    items.append({"item_id": "001", "name": "Pizza", "quantity": item_quantity, "unit_price": 25.00, "total_price": item_quantity * 25.00})
                case '2':
                    items.append({"item_id": "002", "name": "Burger", "quantity": item_quantity, "unit_price": 30.00, "total_price": item_quantity * 30.00})
                case '3':
                    items.append({"item_id": "003", "name": "Salad", "quantity": item_quantity, "unit_price": 15.00, "total_price": item_quantity * 15.00})
                case _:
                    print("Item number not found. Please select either 1, 2, or 3.")
        return customer_name, items

    def place_order(self):
        self.display_menu()
        order_details = self.receive_order()
        order = self.ordering_system.place_order(*order_details)
        print(f"Order placed successfully:\n{order}")
        
    #reservation section of userInterface class
    def receive_reservation(self):
        customer_name = input("Enter customer name: ")
        
        while True:
            reservation_date_str = input("Enter reservation date (YYYY-MM-DD): ")
            try:
                datetime.strptime(reservation_date_str, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        
        while True:
            reservation_time_str = input("Enter reservation time in 24-hour format (HH:MM): ")
            try:
                datetime.strptime(reservation_time_str, '%H:%M')
                break
            except ValueError:
                print("Invalid time format. Please enter the time in HH:MM format.")
        
        reservation_date_str = f"{reservation_date_str} {reservation_time_str}"
        reservation_date = datetime.strptime(reservation_date_str, '%Y-%m-%d %H:%M')
        
        while True:
            try:
                party_size = int(input("Enter party size: "))
                break
            except ValueError:
                print("Invalid input. Please enter an integer value for party size.")
        
        special_requests = input("Enter special requests (optional): ")
        return customer_name, reservation_date, party_size, special_requests

    def make_reservation(self):
        reservation_details = self.receive_reservation()
        reservation = self.reservation_system.make_reservation(*reservation_details)
        print(f"Reservation created successfully:\n{reservation}")
