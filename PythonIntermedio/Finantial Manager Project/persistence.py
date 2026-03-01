import json
import os
import csv
from logic import Transaction, Category



def save_data(manager, folder="data"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    transactions_path = os.path.join(folder, "transactions.json")
    categories_path = os.path.join(folder, "categories.json")

    transactions_data = [t.to_dict() for t in manager.transactions]

    categories_data = {
        name: category.color
        for name, category in manager.categories.items()
    }

    with open(transactions_path, "w", encoding="utf-8") as f:
        json.dump(transactions_data, f, indent=4)

    with open(categories_path, "w", encoding="utf-8") as f:
        json.dump(categories_data, f, indent=4)

def load_data(manager, folder="data"):
    transactions_path = os.path.join(folder, "transactions.json")
    categories_path = os.path.join(folder, "categories.json")

    if os.path.exists(categories_path):
        with open(categories_path, "r", encoding="utf-8") as f:
            categories_data = json.load(f)
            for name, color in categories_data.items():
                manager.categories[name] = Category(name, color)

    if os.path.exists(transactions_path):
        with open(transactions_path, "r", encoding="utf-8") as f:
            transactions_data = json.load(f)
            for item in transactions_data:
                transaction = Transaction(
                    item["date"],
                    item["title"],
                    item["amount"],
                    item["category"],
                    item["type"]
                )
                manager.transactions.append(transaction)

def export_to_csv(manager, filename="financial_report.csv"):
    totals = manager.calculate_totals()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["Date", "Title", "Amount", "Category", "Type"])

        for transaction in manager.transactions:
            writer.writerow([
                transaction.date,
                transaction.title,
                transaction.amount,
                transaction.category,
                transaction.transaction_type
            ])

        writer.writerow([])
        writer.writerow(["Totals"])
        writer.writerow(["Income", totals["income"]])
        writer.writerow(["Expense", totals["expense"]])
        writer.writerow(["Balance", totals["balance"]])