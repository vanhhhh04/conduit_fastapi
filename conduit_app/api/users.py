from fastapi import APIRouter, Depends, HTTPException,Response, status
from models.user import ArticleModel,UserModel
from typing import List,Union,Annotated,Optional
from sqlmodel import Session, select
from models.database import get_session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security import OAuth2
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
import jwt
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from jose import JWTError
from starlette.requests import Request
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_401_UNAUTHORIZED

router = APIRouter()

class CustomizeOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "token":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "token"},
                )
            else:
                return None
        return param


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = CustomizeOAuth2PasswordBearer(tokenUrl="token")
db_dependency = Annotated[Session, Depends(get_session)]

class TokenData(BaseModel):
    email: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    user: UserCreate

class UserResponse(BaseModel):
    email: str
    username: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[str] = None

    class Config:
        orm_mode = True


class UserInDB(UserCreate):
    hashed_password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, email: str) -> Optional[UserModel]:
    statement = select(UserModel).where(UserModel.email == email)
    result = db.exec(statement)
    return result.first()

def authenticate_user(db, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/users")  # Route without the "api" prefix
def register(user: UserLogin, db: db_dependency):
    try:
        # Check if the email already exists
        db_user = get_user(db, user.user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="email already registered")
        # Hash the plain password
        hashed_password = get_password_hash(user.user.password)
        # Create a new user instance
        new_user = UserModel(email=user.user.email, hashed_password=hashed_password)
        # Add the user to the database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        # Create an access token
        access_token = create_access_token(data={"sub": new_user.email})
        return {"user":
            {"email": new_user.email,
             "token": access_token,
             "username": new_user.username,
             "bio": new_user.bio,
             "image": new_user.image}}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"{e}")



@router.post("/users/login")
async def login_for_access_token(
    user_request: UserLogin,
    db: Session = Depends(get_session)
):
    user = authenticate_user(db, user_request.user.email, user_request.user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Token"},
        )
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"user":
            {"email": user.email,
             "token": access_token,
             "username": user.username,
             "bio": user.bio,
             "image": user.image}}


def get_current_user(db: db_dependency, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Token"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/user")
def read_users_me(current_user: user_dependency):
    return {
  "profile": {
    "username": current_user.username,
    "bio": current_user.bio,
    "image": current_user.image,
    "following": None
  }
}



class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[str] = None
    password: Optional[str] = None


class UserUpdate(BaseModel):
    user : UserUpdate


@router.put("/user")
def update_user(
    current_user: user_dependency,
    user_request: UserUpdate,
    db: Session = Depends(get_session)
):
    # Create a dictionary of the fields to update
    update_data = user_request.user.dict(exclude_unset=True)

    # Update fields on the current_user object
    for name, value in update_data.items():
        if name == "password":
            setattr(current_user, "hashed_password", get_password_hash(value))
        elif value is not None:
            setattr(current_user, name, value)

    # Commit the changes to the database
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return {"message": "Update successful"}

