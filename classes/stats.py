
from datetime import datetime


class Stats:
    def __init__(self, database):
        self.database = database

    def generate_report(self, sales, date):
        if not sales:
            return "No sales data available."

        report = [] #initialises report structure
        report.append(f"Sales Reports for {date.strftime('%Y-%m')}")
        report.append("----------------------------")
        
        sales_found = False
        for sale in sales["sales"]:
            sale_date = datetime.strptime(sale["date"], "%Y-%m-%d")
            if sale_date.year == date.year and sale_date.month == date.month:
                sales_found = True
                items = ", ".join([f"{item['item_id']} (qty: {item['quantity']})" for item in sale["items"]])
                report.append(f"{sale['date']} - Items: {items}") #appends item data to report
        
        if not sales_found:
            return None  

        return "\n".join(report)
    
    def print_report(self):
        sales = self.database.report_sales
        if not sales: #if sales.json is empty
            print("No sales data found")
            return

        while True:
            x = input("What month and year would you like to print? (e.g., 2024-05 or type 'exit' to quit): ").lower()
            if x in ['exit', 'escape', 'quit', 'q']: #multiple ways to escape
                break

            try:
                filter_date = datetime.strptime(x, "%Y-%m")
                filtered_report = self.generate_report(sales, filter_date) #generates report based on date provided by user
                if filtered_report is None:
                    print(f"No sales found for {filter_date.strftime('%Y-%m')}.") #provides error message if no sales are found for filtered date
                    continue

                print(filtered_report)
                export_report = input("Would you like to save this report to a .txt file? (yes/no): ").lower() #provides option to create .txt file
                if export_report in ['yes', 'y']:
                    file_name = f"sales_report_{filter_date.strftime('%Y-%m')}.txt" #exports sales based on date provided - labels accordingly 
                    with open(file_name, "w") as file:
                        file.write(filtered_report)
                    print(f"Report saved to {file_name}")

            except ValueError:
                print("Invalid date format. Please use YYYY-MM.") #gives error message if date does not match pattern
