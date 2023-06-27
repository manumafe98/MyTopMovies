from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from passlib.context import CryptContext
from jose import JWTError, jwt

SECRET_KEY = "d49d7d6d99038b8ff86ccff9a2de01f360f29fff0344ab7027c072291e83509c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/signin")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user):
    try:
        payload = {"username": user.username, "email": user.email}
        return jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)
    except Exception as ex:
        raise ex


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, key=SECRET_KEY)
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Could not validate credentials", 
                            headers={"WWW-Authenticate": "Bearer"})