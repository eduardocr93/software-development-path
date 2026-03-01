import pytest
from logic import FinanceManager


def test_add_category():
    manager = FinanceManager()
    manager.add_category("Food")

    assert "Food" in manager.categories
    
def test_duplicate_category():
    manager = FinanceManager()
    manager.add_category("Food")
    
    with pytest.raises(ValueError):
        manager.add_category("Food")

def test_add_transaction_without_categories():
    manager = FinanceManager()

    with pytest.raises(ValueError):
        manager.add_transaction("01/01/2026", "Test", 100, "Food", "Income")

def test_invalid_date_format():
    manager = FinanceManager()
    manager.add_category("Food")

    with pytest.raises(ValueError):
        manager.add_transaction("2026-01-01", "Test", 100, "Food", "Income")

def test_future_date():
    manager = FinanceManager()
    manager.add_category("Food")

    with pytest.raises(ValueError):
        manager.add_transaction("01/01/3000", "Test", 100, "Food", "Income")

def test_negative_amount():
    manager = FinanceManager()
    manager.add_category("Food")

    with pytest.raises(ValueError):
        manager.add_transaction("01/01/2026", "Test", -50, "Food", "Income")

def test_calculate_totals():
    manager = FinanceManager()
    manager.add_category("Food")
    manager.add_category("Salary")

    manager.add_transaction("01/01/2026", "Paycheck", 1000, "Salary", "Income")
    manager.add_transaction("02/01/2026", "Pizza", 100, "Food", "Expense")

    totals = manager.calculate_totals()

    assert totals["income"] == 1000
    assert totals["expense"] == 100
    assert totals["balance"] == 900

def test_filter_by_date():
    manager = FinanceManager()
    manager.add_category("Food")

    manager.add_transaction("01/01/2026", "A", 100, "Food", "Income")
    manager.add_transaction("10/01/2026", "B", 50, "Food", "Expense")

    filtered = manager.filter_by_date("01/01/2026", "05/01/2026")

    assert len(filtered) == 1
    assert filtered[0].title == "A"

def test_invalid_date_range():
    manager = FinanceManager()

    with pytest.raises(ValueError):
        manager.filter_by_date("10/01/2026", "01/01/2026")