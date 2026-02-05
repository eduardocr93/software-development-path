class BankAccount():
    def __init__(self, balance=0):
        self.balance = balance

    def substract_balance(self, amount):
        self.balance -= amount
        print(f"Retiro realizado! Su balance es de ${self.balance}")
    
    def add_balance(self, amount):
        self.balance += amount
        print(f"Deposito realizado! Su balance es de ${self.balance}")

class SavingAccount(BankAccount):
    def __init__(self, balance=0, min_balance=0):
        super().__init__(balance)
        self.min_balance = min_balance

    def substract_balance(self,amount):
        if self.balance - amount < self.min_balance:
            raise ValueError(f"No se puede retirar ${amount}. El Balance no puede bajar de ${self.min_balance}")
        super().substract_balance(amount)

account = SavingAccount(balance=100, min_balance=50)

try:
    account.add_balance(20)     
    account.substract_balance(40)
    account.substract_balance(40)
except ValueError as e:
    print(f"Error: {e}")
