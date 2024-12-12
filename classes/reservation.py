
from datetime import datetime

class Reservation:
    def __init__(self, reservation_id, customer_name, reservation_date, party_size, special_requests=None):
        self.reservation_id = reservation_id
        self.customer_name = customer_name
        self.reservation_date = reservation_date
        self.party_size = party_size
        self.special_requests = special_requests

    def __str__(self):
        return (f"Reservation ID: {self.reservation_id}\n"
                f"Customer Name: {self.customer_name}\n"
                f"Reservation Date: {self.reservation_date}\n"
                f"Party Size: {self.party_size}\n"
                f"Special Requests: {self.special_requests}")

    def to_dict(self):
        return {
            "reservation_id": self.reservation_id,
            "customer_name": self.customer_name,
            "reservation_date": self.reservation_date.strftime('%Y-%m-%d %H:%M:%S'),
            "party_size": self.party_size,
            "special_requests": self.special_requests
        }

    @staticmethod
    def from_dict(data):
        return Reservation(
            reservation_id=data["reservation_id"],
            customer_name=data["customer_name"],
            reservation_date=datetime.strptime(data["reservation_date"], '%Y-%m-%d %H:%M:%S'),
            party_size=data["party_size"],
            special_requests=data.get("special_requests")
        )
    
class Reservations:
    def __init__(self, database):
        self.database = database
        self.next_id = max(self.database.reservations.keys(), default=0) + 1

    def make_reservation(self, customer_name, reservation_date, party_size, special_requests=None):
        reservation_id = self.next_id
        self.next_id += 1
        new_reservation = Reservation(reservation_id, customer_name, reservation_date, party_size, special_requests)
        self.database.add_reservation(new_reservation)
        return new_reservation