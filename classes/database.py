import json
from reservation import Reservation
from order import Order

class Database:
    def __init__(self, sales_file="db/sales.json", reservations_file='db/reservations.json'):
        self.sales_file = sales_file
        self.reservations_file = reservations_file
        self.sales = self.load_sales()
        self.report_sales = self.load_report_sales()
        self.reservations = self.load_reservations()

    #sales section of database class
    def load_sales(self):
        try:
            with open(self.sales_file, 'r') as file:
                data = json.load(file)
                return [Order.from_dict(sale) for sale in data["sales"]]
        except FileNotFoundError:
            return []

    def save_sales(self):
        with open(self.sales_file, 'w') as file:
            json.dump({"sales": [sale.to_dict() for sale in self.sales]}, file, indent=4)

    def add_sale(self, sale):
        self.sales.append(sale)
        self.save_sales()

    #reservation section of database class
    def load_reservations(self):
        try:
            with open(self.reservations_file, 'r') as file:
                data = json.load(file)
                return {int(k): Reservation.from_dict(v) for k, v in data.items()}
        except FileNotFoundError:
            return {}

    def save_reservations(self):
        with open(self.reservations_file, 'w') as file:
            json.dump({k: v.to_dict() for k, v in self.reservations.items()}, file, indent=4)

    def query_reservation(self, reservation_id):
        return self.reservations.get(reservation_id)

    def add_reservation(self, reservation):
        self.reservations[reservation.reservation_id] = reservation
        self.save_reservations()

    #sales report section of database class
    def load_report_sales(self):
        try:
            with open("db/sales.json") as j: #simple load of sales data
                sales = json.load(j)
        except FileNotFoundError:
            sales = None
            print("Sales not found") #returns error message if sales.json is empty
        return sales
