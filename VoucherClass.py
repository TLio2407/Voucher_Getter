class Voucher:
    def __init__(self, id, type, start_date, end_date):
        self.id = id
        self.type = type.strip().split("AFF_")[1]
        self.start_date = start_date
        self.end_date = end_date

    def is_valid(self, current_date):
        return current_date <= self.end_date
    
    def valid_day_left(self, current_date):
        if self.is_valid(current_date):
            return (self.end_date - current_date).days
        return 0
    
    def print_details(self):
        print(f"Voucher ID: {self.id}")
        print(f"Type: {self.type}")
        print(f"Start Date: {self.start_date}")
        print(f"End Date: {self.end_date}")
        print("-" * 20)
    