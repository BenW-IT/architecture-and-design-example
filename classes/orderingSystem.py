from datetime import datetime
from order import Order

class OrderingSystem:
    def __init__(self, database):
        self.database = database
        self.next_id = max([int(sale.sale_id) for sale in self.database.sales], default=0) + 1

    def place_order(self, customer_name, items):
        sale_id = str(self.next_id).zfill(3)
        self.next_id += 1
        date = datetime.now()
        total_amount = sum(item["quantity"] * item["unit_price"] for item in items)
        new_order = Order(sale_id, date, customer_name, items, total_amount)
        self.database.add_sale(new_order)
        return new_order

