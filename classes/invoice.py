from datetime import datetime
import os
from database import Database

class Invoice:
    def __init__(self, database):
        self.database = database

    def generate_invoice(self, customer_name):
        orders = [order for order in self.database.sales if order.customer_name.lower() == customer_name.lower()]

        if not orders:
            print(f"No orders found for customer: {customer_name}")
            return

        invoice_content = []
        total_amount = 0

        invoice_content.append(f"Invoice for {customer_name}")
        invoice_content.append("="*40)

        for order in orders:
            invoice_content.append(f"Order ID: {order.sale_id} | Date: {order.date.strftime('%Y-%m-%d')}")
            for item in order.items:
                invoice_content.append(f"  - {item['quantity']} x {item['name']} @ ${item['unit_price']} each = ${item['total_price']:.2f}")
            total_amount += order.total_amount
            invoice_content.append("-"*40)

        invoice_content.append(f"Total Amount Due: ${total_amount:.2f}")
        invoice_content.append("="*40)

        invoice_text = "\n".join(invoice_content)
        print(invoice_text)

        print_receipt_option = input("Would you like to print a receipt? (yes/no): ").lower()
        if print_receipt_option in ['yes', 'y']:
            self.generate_receipt(customer_name)

    def generate_receipt(self, customer_name):
        orders = [order for order in self.database.sales if order.customer_name.lower() == customer_name.lower()]

        if not orders:
            print(f"No orders found for customer: {customer_name}")
            return

        receipt_content = []
        total_amount = 0

        receipt_content.append(f"Receipt for {customer_name}")
        receipt_content.append("="*40)

        for order in orders:
            receipt_content.append(f"Order ID: {order.sale_id} | Date: {order.date.strftime('%Y-%m-%d')}")
            for item in order.items:
                receipt_content.append(f"  - {item['quantity']} x {item['name']} @ ${item['unit_price']} each = ${item['total_price']:.2f}")
            total_amount += order.total_amount
            receipt_content.append("-"*40)

        receipt_content.append(f"Total Amount Paid: ${total_amount:.2f}")
        receipt_content.append("="*40)

        receipt_text = "\n".join(receipt_content)
        print(receipt_text)

        # Ensure the receipts directory exists
        if not os.path.exists('receipts'):
            os.makedirs('receipts')

        file_name = f"receipts/receipt_{customer_name.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        with open(file_name, "w") as file:
            file.write(receipt_text)
        print(f"Receipt saved to {file_name}")

# Example usage
if __name__ == "__main__":
    database = Database()
    invoice = Invoice(database)
    customer_name = input("Enter the customer name for the invoice: ")
    invoice.generate_invoice(customer_name)
