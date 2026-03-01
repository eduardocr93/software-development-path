import FreeSimpleGUI as sg
from logic import FinanceManager
from persistence import load_data, save_data, export_to_csv
from datetime import datetime


def create_main_window(manager):
    headings = ["Date", "Title", "Amount", "Category", "Type"]

    layout = [
        [sg.Text("Personal Finance Manager", font=("Arial", 16))],

        [
            sg.Text("Start Date"),
            sg.Input(key="-START-", size=(12,1), readonly=True),
            sg.CalendarButton("Select", target="-START-", format="%d/%m/%Y"),

            sg.Text("End Date"),
            sg.Input(key="-END-", size=(12,1), readonly=True),
            sg.CalendarButton("Select", target="-END-", format="%d/%m/%Y"),

            sg.Button("Filter"),
            sg.Button("Clear Filter")
        ],

        [
            sg.Table(
                values=[],
                headings=headings,
                key="-TABLE-",
                auto_size_columns=True,
                expand_x=True,
                expand_y=True,
                justification="center"
            )
        ],

        [
            sg.Button("Add Category"),
            sg.Button("Add Expense"),
            sg.Button("Add Income"),
            sg.Button("Export CSV"),
            sg.Button("Exit")
        ]
    ]

    return sg.Window("Finance Manager", layout, resizable=True, finalize=True)


def update_table(window, manager, transactions=None):
    if transactions is None:
        transactions = manager.transactions

    data = []
    row_colors = []

    for i, t in enumerate(transactions):
        data.append([
            t.date,
            t.title,
            t.amount,
            t.category,
            t.transaction_type
        ])

        category_obj = manager.categories.get(t.category)

        if category_obj:
            row_colors.append((i, "black", category_obj.color))

    window["-TABLE-"].update(
        values=data,
        row_colors=row_colors
    )


def run_app():
    manager = FinanceManager()
    load_data(manager)

    window = create_main_window(manager)
    update_table(window, manager)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            save_data(manager)
            break

        if event == "Filter":
            try:
                start = values["-START-"]
                end = values["-END-"]

                if not start or not end:
                    sg.popup("Please select both dates.")
                else:
                    filtered = manager.filter_by_date(start, end)
                    update_table(window, manager, filtered)

            except Exception as e:
                sg.popup(f"Error: {e}")

        if event == "Clear Filter":
            update_table(window, manager)

        if event == "Add Category":
            add_category_window(manager)

        if event == "Add Income":
            if not manager.categories:
                sg.popup("You must create a category first.")
            else:
                add_income_window(manager)
                update_table(window, manager)

        if event == "Add Expense":
            add_expense_window(manager)
            update_table(window, manager)

        if event == "Export CSV":
            export_to_csv(manager)
            sg.popup("CSV exported successfully!")

    window.close()

def add_category_window(manager):
    layout = [
        [sg.Text("Category Name")],
        [sg.Input(key="-CATEGORY-")],

        [sg.Text("Color")],
        [
            sg.Input(key="-COLOR-", size=(10,1), readonly=True),
            sg.ColorChooserButton("Choose Color", target="-COLOR-")
        ],

        [sg.Button("Save"), sg.Button("Cancel")]
    ]

    window = sg.Window("Add Category", layout, modal=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Cancel"):
            break

        if event == "Save":
            category = values["-CATEGORY-"].strip()
            color = values["-COLOR-"]

            if category and color:
                try:
                    manager.add_category(category, color)
                    sg.popup("Category added successfully!")
                    break
                except Exception as e:
                    sg.popup(f"Error: {e}")
            else:
                sg.popup("Category and color are required")

    window.close()

def add_income_window(manager):
    today = datetime.now().strftime("%d/%m/%Y")
    layout = [
        [sg.Text("Date"),
        sg.Input(default_text=today, key="-DATE-", size=(12,1), readonly=True),
        sg.CalendarButton("Select Date", target="-DATE-", format="%d/%m/%Y")],
        [sg.Text("Title"), sg.Input(key="-TITLE-")],
        [sg.Text("Amount"), sg.Input(key="-AMOUNT-")],
        [sg.Text("Category"), sg.Combo(list(manager.categories.keys()), key="-CATEGORY-")],
        [sg.Button("Save"), sg.Button("Cancel")]
    ]

    window = sg.Window("Add Income", layout, modal=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Cancel"):
            break

        if event == "Save":
            try:
                manager.add_transaction(
                    values["-DATE-"],
                    values["-TITLE-"],
                    float(values["-AMOUNT-"]),
                    values["-CATEGORY-"],
                    "Income"
                )
                sg.popup("Income added successfully!")
                break
            except Exception as e:
                sg.popup(f"Error: {e}")

    window.close()

def add_expense_window(manager):
    today = datetime.now().strftime("%d/%m/%Y")
    layout = [
        [sg.Text("Date"),
        sg.Input(default_text=today, key="-DATE-", size=(12,1), readonly=True),
        sg.CalendarButton("Select Date", target="-DATE-", format="%d/%m/%Y")],
        [sg.Text("Title"), sg.Input(key="-TITLE-")],
        [sg.Text("Amount"), sg.Input(key="-AMOUNT-")],
        [sg.Text("Category"), sg.Combo(list(manager.categories.keys()), key="-CATEGORY-")],
        [sg.Button("Save"), sg.Button("Cancel")]
    ]

    window = sg.Window("Add Expense", layout, modal=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Cancel"):
            break

        if event == "Save":
            try:
                manager.add_transaction(
                    values["-DATE-"],
                    values["-TITLE-"],
                    float(values["-AMOUNT-"]),
                    values["-CATEGORY-"],
                    "Expense"
                )
                sg.popup("Expense added successfully!")
                break
            except Exception as e:
                sg.popup(f"Error: {e}")

    window.close()