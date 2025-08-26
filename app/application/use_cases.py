from typing import List, Tuple
from ..domain.entities import User
from ..domain.repositories import UserRepository
from ..domain.exceptions import UserNotFound, EmailAlreadyExists, InvalidTransfer, InsufficientFunds


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, name: str, email: str, balance: float) -> User:
        if self.user_repository.find_by_email(email):
            raise EmailAlreadyExists(f"Email {email} already exists")
        
        user = User(id=None, name=name, email=email, balance=balance)
        return self.user_repository.save(user)


class GetUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self) -> List[User]:
        return self.user_repository.find_all()


class TransferMoneyUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, from_user_id: int, to_user_id: int, amount: float) -> Tuple[User, User]:
        if from_user_id == to_user_id:
            raise InvalidTransfer("Cannot transfer to the same user")
        
        if amount <= 0:
            raise InvalidTransfer("Amount must be positive")

        from_user = await self.user_repository.find_by_id(from_user_id)
        if not from_user:
            raise UserNotFound(f"User {from_user_id} not found")

        to_user = await self.user_repository.find_by_id(to_user_id)
        if not to_user:
            raise UserNotFound(f"User {to_user_id} not found")

        if not from_user.can_transfer(amount):
            raise InsufficientFunds("Insufficient funds")

        from_user.debit(amount)
        to_user.credit(amount)

        updated_from = self.user_repository.save(from_user)
        updated_to = self.user_repository.save(to_user)

        return updated_from, updated_to