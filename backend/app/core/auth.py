from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import User
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


def get_current_user(request: Request, db: Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = request.cookies.get("access_token")

    if token is None:
        raise HTTPException(status_code=401, detail="User not authenticated")

    try:
        payload = verify_refresh_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise


@router.post("/token")
def login_for_access_token(response: Response, login_data: LoginRequest, db: Session = Depends(get_db)):
    print("ciao")
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # !!!! DA MODIFICARE IN TRUE IN PRODUZIONE
        samesite="lax",
        max_age=1800  # 30 minuti
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # !!!! DA MODIFICARE IN TRUE IN PRODUZIONE
        samesite="lax",
        max_age=604800  # 7 giorni
    )

    return {"user": {"email": user.email, "is_admin": user.is_admin}}


@router.post("/refresh")
def refresh_access_token(request: Request, response: Response):

    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token mancante")

    try:
        payload = verify_refresh_token(refresh_token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token(data={"sub": email})
    new_refresh_token = create_refresh_token(data={"sub": email})

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=False,  # !!!! DA MODIFICARE IN TRUE IN PRODUZIONE
        samesite="lax",
        max_age=1800
    )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False,  # !!!! DA MODIFICARE IN TRUE IN PRODUZIONE
        samesite="lax",
        max_age=604800
    )

    return {"msg": "Token aggiornati"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token", samesite="lax")
    response.delete_cookie(key="refresh_token", samesite="lax")
    return {"msg": "Logout effettuato"}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "is_admin": current_user.is_admin}
