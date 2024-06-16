from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from config.database import get_db
import models.models as models
from schemas.schemas import UserAuth, UserCreate, UserResponse
from functions_jwt import write_token, validate_token
from typing import Dict

auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Variables globales para almacenar temporalmente el token
token_storage: Dict[str, str] = {"access_token": "", "token_type": ""}

# Variable global para almacenar user_data temporalmente
user_data_store: Dict[str, Dict] = {}

# Utility function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Utility function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Register route
@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = models.User(
        email=user.email,
        password=hashed_password,
        role=user.role,
        firstName=user.firstName,
        lastName=user.lastName,
        phone=user.phone,
        birthdate=user.birthdate,
        avatar=user.avatar,
        description=user.description,
        rating=user.rating,
        ubicationId=user.ubicationId
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Login route
@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(user: UserAuth, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).filter(models.User.role == user.role).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    token = write_token({
        "id": db_user.id,
        "email": db_user.email,
        "role": db_user.role,
        "firstName": db_user.firstName,
        "lastName": db_user.lastName,
        "phone": db_user.phone,
        "birthdate": str(db_user.birthdate),
        "avatar": db_user.avatar,
        "description": db_user.description,
        "rating": db_user.rating,
        "ubicationId": db_user.ubicationId
    })  # Generar el token JWT

      # Almacenar el token en la variable global
    token_storage["access_token"] = token
    token_storage["token_type"] = "bearer"

    return {"access_token": token, "token_type": "bearer"}

# Endpoint GET para mostrar los valores del token
@auth_router.get("/token_info", status_code=status.HTTP_200_OK)
def token_info():
    return token_storage

async def get_current_user(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header format")
    token = parts[1]
    if token not in user_data_store:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found or invalid")
    return user_data_store[token]

@auth_router.post("/verify/token")
async def verify_token(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header format")
    token = parts[1]
    try:
        user_data = validate_token(token, output=True)
        user_data_store[token] = user_data  # Guardar user_data usando el token como clave
        return user_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token validation failed: {str(e)}")


@auth_router.get("/user/data")
async def get_user_data(current_user: Dict = Depends(get_current_user)):
    return current_user
