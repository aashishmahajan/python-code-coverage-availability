import pytest
from src.yet_another.account_operations import BankAccount


def test_account_creation():
    """Tests account creation with a name and initial balance."""
    account = BankAccount("Alice", 100)
    assert account.name == "Alice"
    assert account.balance == 100


def test_deposit():
    """Tests depositing funds into the account."""
    account = BankAccount("Bob")
    account.deposit(50)
    assert account.balance == 50


def test_withdraw():
    """Tests withdrawing funds from the account."""
    account = BankAccount("Charlie", 200)
    account.withdraw(100)
    assert account.balance == 100


# def test_withdraw_insufficient_funds():
#     """Tests attempting to withdraw more than the available balance."""
#     account = BankAccount("David", 50)
#     with pytest.raises(Exception) as excinfo:
#         account.withdraw(100)
#     assert "Insufficient funds" in str(excinfo.value)


def test_get_balance():
    """Tests retrieving the account balance."""
    account = BankAccount("Emily", 300)
    assert account.get_balance() == 300
