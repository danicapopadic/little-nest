from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from little_nest.database import get_db
from little_nest.schemas.user import UserCreate, UserResponse
from little_nest.services.user import EmailAlreadyExistsError, register_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"description": "Email already registered"},
    },
)
def register(
    data: UserCreate,
    db: Annotated[Session, Depends(get_db)],
) -> UserResponse:
    try:
        user = register_user(db, data)
    except EmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        ) from exc

    return UserResponse.model_validate(user)
