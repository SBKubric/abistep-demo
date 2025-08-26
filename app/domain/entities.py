from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    name: str
    email: str
    balance: float

    def __post_init__(self):
        if self.balance < 0:
            raise ValueError("Balance cannot be negative")

    def can_transfer(self, amount: float) -> bool:
        return self.balance >= amount and amount > 0

    def debit(self, amount: float) -> None:
        if not self.can_transfer(amount):
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def credit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount