from pydantic import BaseModel, EmailStr, Field
from typing import List


class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    balance: float = Field(..., ge=0)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    balance: float


class TransferRequest(BaseModel):
    from_user_id: int = Field(..., gt=0)
    to_user_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)


class TransferResponse(BaseModel):
    from_user: UserResponse
    to_user: UserResponse


class ErrorResponse(BaseModel):
    detail: str