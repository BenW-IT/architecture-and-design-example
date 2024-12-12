import json
from database import Database
from userInterface import UserInterface
from invoice import Invoice
from pyfiglet import Figlet

class KoalaSystem:
    def __init__(self, user_interface):
        self.user_interface = user_interface
        self.invoice = Invoice(user_interface.database)

    @staticmethod
    def login_details(account_file):
        try:
            with open(account_file, 'r') as file:
                account_details = json.load(file)
            return account_details
        except FileNotFoundError:
            print(f"Error: The file {account_file} was not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: The file {account_file} contains invalid JSON.")
            return None

    @staticmethod
    def login(account_details):
        while True:
            username = input("Enter username: ")
            password = input("Enter password: ")
            if username == account_details["username"] and password == account_details["password"]:
                print("Login successful!")
                return True
            else:
                print("Invalid username or password. Try again.")

    def start(self):
        while True:
            print("Enter:\n- 'order' to place an order\n- 'reservation' to make a reservation\n- 'report' to print sales reports\n- 'invoice' to generate an invoice")
            choice = input("or 'exit' to quit: ").lower()
            match choice:
                case 'order':
                    self.user_interface.place_order()
                case 'reservation':
                    self.user_interface.make_reservation()
                case 'report':
                    self.user_interface.report.print_report()
                case 'invoice':
                    customer_name = input("Enter the customer name for the invoice: ")
                    self.invoice.generate_invoice(customer_name)
                case 'exit' | 'quit':
                    break
                case _:
                    print("Unrecognized command")

    @staticmethod
    def main():
        f = Figlet(font='doom')
        print(f.renderText('Koala Cafe'))
        account_details = KoalaSystem.login_details("db/login.json")
        if not account_details:
            return

        while not KoalaSystem.login(account_details):
            pass
        
        # Initialize Database and UserInterface
        database = Database()
        user_interface = UserInterface(database)
        
        # Start main system
        KoalaSystem(user_interface).start()

if __name__ == "__main__":
    KoalaSystem.main()
