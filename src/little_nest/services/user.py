from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from little_nest.models.user import User
from little_nest.schemas.user import UserCreate
from little_nest.security import hash_password


class EmailAlreadyExistsError(Exception):
    pass


def register_user(db: Session, data: UserCreate) -> User:
    user = User(
        name=data.name,
        email=data.email.lower(),
        password_hash=hash_password(data.password),
    )

    db.add(user)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()

        if (
            isinstance(exc.orig, UniqueViolation)
            and exc.orig.diag.constraint_name == "uq_users_email"
        ):
            raise EmailAlreadyExistsError() from exc

        raise

    db.refresh(user)

    return user
