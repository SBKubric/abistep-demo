from ..domain.entities import User
from ..domain.repositories import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users: dict[int, User] = {}
        self._user_emails: dict[str, int] = {}
        self._next_id = 1

    async def save(self, user: User) -> User:
        if user.email in self._user_emails and self._user_emails[user.email] != user.id:
            raise ValueError(f"Email {user.email} already exists")
        if user.id is None:
            user.id = self._next_id
            self._next_id += 1
        self._users[user.id] = user
        self._user_emails[user.email] = user.id
        return user

    async def find_by_id(self, user_id: int) -> User | None:
        return self._users.get(user_id)

    async def find_by_email(self, email: str) -> User | None:
        user_id: int = self._user_emails.get(email, -1)
        return self._users.get(user_id)

    async def find_all(self) -> list[User]:
        return list(self._users.values())
