from Config import Security
from Config.Database import get_db
from Config.Model import User
from jose import JWTError, jwt
from Config.Schemas import TokenData, UserCreate
from Crud.User_crud import create_user, get_user_by_email, get_user_by_name
from fastapi import Depends, HTTPException, status


async def get_current_user(
    db=Depends(get_db), token: str = Depends(Security.oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, Security.SECRET_KEY, algorithms=[Security.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        permissions: str = payload.get("permissions")
        token_data = TokenData(email=email, permissions=permissions)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


def authenticate_user(db, username: str, password: str):
    user = get_user_by_name(db, username)
    if not user:
        return False
    if not Security.verify_password(password, user.password):
        return False
    return user


def sign_up_new_user(db, username: str, password: str, email: str, contact: str):
    user = get_user_by_email(db, username)
    if user:
        return False  # User already exists
    new_user = create_user(
        db,
        UserCreate(
            email=email,
            password=password,
            name=username,
            contact=contact
        ),
    )
    return new_user