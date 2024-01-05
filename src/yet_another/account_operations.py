class BankAccount:
    """Represents a bank account with basic operations."""

    def __init__(self, name, initial_balance=0):
        """Initializes the account with a name and initial balance."""
        self.name = name
        self.balance = initial_balance

    def deposit(self, amount):
        """Deposits the specified amount into the account."""
        self.balance += amount
        print(f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}")

    def withdraw(self, amount):
        """Withdraws the specified amount from the account, if possible."""
        if amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            print(f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")

    def get_balance(self):
        """Returns the current account balance."""
        return self.balance
