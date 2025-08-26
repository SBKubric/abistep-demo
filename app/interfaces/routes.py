from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .schemas import CreateUserRequest, UserResponse, TransferRequest, TransferResponse
from ..application.use_cases import (
    CreateUserUseCase,
    GetUsersUseCase,
    TransferMoneyUseCase,
)
from ..domain.exceptions import (
    EmailAlreadyExists,
    UserNotFound,
    InvalidTransfer,
    InsufficientFunds,
)
from ..infrastructure.repositories import InMemoryUserRepository

user_repository = InMemoryUserRepository()


def get_create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase(user_repository)


def get_users_use_case() -> GetUsersUseCase:
    return GetUsersUseCase(user_repository)


def get_transfer_use_case() -> TransferMoneyUseCase:
    return TransferMoneyUseCase(user_repository)


router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    request: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
):
    try:
        user = await use_case.execute(request.name, request.email, request.balance)
        return UserResponse(
            id=user.id, name=user.name, email=user.email, balance=user.balance
        )
    except EmailAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users", response_model=List[UserResponse])
async def get_users(use_case: GetUsersUseCase = Depends(get_users_use_case)):
    users = await use_case.execute()
    return [
        UserResponse(id=u.id, name=u.name, email=u.email, balance=u.balance)
        for u in users
    ]


@router.post("/transfer", response_model=TransferResponse)
async def transfer_money(
    request: TransferRequest,
    use_case: TransferMoneyUseCase = Depends(get_transfer_use_case),
):
    try:
        from_user, to_user = await use_case.execute(
            request.from_user_id, request.to_user_id, request.amount
        )
        return TransferResponse(
            from_user=UserResponse(
                id=from_user.id,
                name=from_user.name,
                email=from_user.email,
                balance=from_user.balance,
            ),
            to_user=UserResponse(
                id=to_user.id,
                name=to_user.name,
                email=to_user.email,
                balance=to_user.balance,
            ),
        )
    except (UserNotFound, InvalidTransfer, InsufficientFunds) as e:
        raise HTTPException(status_code=400, detail=str(e))
