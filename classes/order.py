
from datetime import datetime

class Order:
    def __init__(self, sale_id, date, customer_name, items, total_amount):
        self.sale_id = sale_id
        self.date = date
        self.customer_name = customer_name
        self.items = items
        self.total_amount = total_amount

    def __str__(self):
        items_str = "\n".join([f"{item['quantity']}x {item['name']} @ ${item['unit_price']} each" for item in self.items])
        return (f"Sale ID: {self.sale_id}\n"
                f"Date: {self.date}\n"
                f"Customer Name: {self.customer_name}\n"
                f"Items:\n{items_str}\n"
                f"Total Amount: ${self.total_amount:.2f}")

    def to_dict(self):
        return {
            "sale_id": self.sale_id,
            "date": self.date.strftime('%Y-%m-%d'),
            "customer": {
                "name": self.customer_name
            },
            "items": self.items,
            "total_amount": self.total_amount
        }

    @staticmethod
    def from_dict(data):
        return Order(
            sale_id=data["sale_id"],
            date=datetime.strptime(data["date"], '%Y-%m-%d'),
            customer_name=data["customer"]["name"],
            items=data["items"],
            total_amount=data["total_amount"]
        )
