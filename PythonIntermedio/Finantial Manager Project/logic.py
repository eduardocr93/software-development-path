from datetime import datetime

class Category:
    def __init__(self, name, color):
        self.name = name
        self.color = color

class Transaction:
    def __init__(self, date, title, amount, category, transaction_type):
        self.date = date
        self.title = title
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
    
    def to_dict(self):
        return {
            "date": self.date,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "type": self.transaction_type
        }


class FinanceManager:
    def __init__(self):
        self.transactions = []
        self.categories = {}

    def add_category(self, name, color="#FFFFFF"):
        if name in self.categories:
            raise ValueError("Category already exists.")
        self.categories[name] = Category(name,color)
    
    def validate_date(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use dd/mm/yyyy.")

        if date_obj > datetime.now():
            raise ValueError("Date cannot be in the future.")
    
    def add_transaction(self, date, title, amount, category, transaction_type):

        if not self.categories:
            raise ValueError("No categories available.")

        self.validate_date(date)

        if not title or not title.strip():
            raise ValueError("Title cannot be empty.")

        title = title.strip()

        if category not in self.categories:
            raise ValueError("Category does not exist.")

        if transaction_type not in ["Income", "Expense"]:
            raise ValueError("Invalid transaction type.")

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if transaction_type == "Expense":
            amount = -abs(amount)

        transaction = Transaction(date, title, amount, category, transaction_type)
        self.transactions.append(transaction)
    
    def calculate_totals(self):
        total_income = 0
        total_expense = 0

        for transaction in self.transactions:
            if transaction.transaction_type == "Income":
                total_income += transaction.amount
            else:
                total_expense  += abs(transaction.amount)
        balance = total_income - total_expense

        return {
            "income": total_income,
            "expense": total_expense,
            "balance": balance
        }
    
    def filter_by_date(self, start_date, end_date):
        try:
            start = datetime.strptime(start_date, "%d/%m/%Y")
            end = datetime.strptime(end_date, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use dd/mm/yyyy.")

        if start > end:
            raise ValueError("Start date cannot be after end date.")

        filtered = []

        for transaction in self.transactions:
            transaction_date = datetime.strptime(transaction.date, "%d/%m/%Y")
            if start <= transaction_date <= end:
                filtered.append(transaction)

        return filtered