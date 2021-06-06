from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.settings import settings
from app.utils import security
from app.database.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


class GetCurrentUser:
    roles = ['default', 'reviewer', 'admin', 'super_admin']

    def __init__(self, min_role_allowed: str = 'default'):
        self.min_role_allowed = min_role_allowed

    def __call__(self, user: models.User = Depends(get_current_active_user)):
        if self.roles.index(user.role.value) < self.roles.index(self.min_role_allowed):
            raise HTTPException(
                status_code=403, detail="The user doesn't have enough privileges")
        return user

# class GetCurrentUser:
#     roles = ['default', 'reviewer', 'admin', 'super_admin']

#     def __init__(self, allowed_roles: List = ['default']):
#         self.allowed_roles = allowed_roles

#     def __call__(self, user: models.User = Depends(get_current_active_user)):
#         if user.role not in self.allowed_roles:
#             raise HTTPException(
#                 status_code=403, detail="The user doesn't have enough privileges")
#         return user
