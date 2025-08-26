from typing import Dict, List, Optional
from ..domain.entities import User
from ..domain.repositories import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users: dict[int, User] = {}
        self._user_mails: set[str] = set()
        self._next_id = 1

    async def save(self, user: User) -> User:
        if user.email in self._user_mails:
            raise ValueError(f"User with email {user.email} already exists")
        if user.id is None:
            user.id = self._next_id
            self._next_id += 1
        self._users[user.id] = user
        self._user_mails.add(user.email)
        return user

    async def find_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    async def find_by_email(self, email: str) -> Optional[User]:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    async def find_all(self) -> List[User]:
        return list(self._users.values())