from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
import logging
from fastapi import HTTPException, Header

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

try: 
    SECRET_KEY= os.environ["SECRET_KEY"]
except Exception as e: 
    logger.error(f"Error getting secret key: {e}")

ALGORITHM = "HS256"
DURATION = 1800

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str: 
    try: 
        return pwd_context.hash(password)
    except Exception as e: 
        logger.error(f"Error hashing password: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
def verify_password(plain: str, hashed: str) -> bool: 
    try: 
        return pwd_context.verify(plain, hashed)
    except Exception as e: 
        logger.error(f"Error verifying password: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
def create_access_token(data: dict) -> str: 
    try: 
        to_encode = data.copy()
        expiration = datetime.utcnow() + timedelta(seconds=DURATION)
        to_encode.update({"exp": expiration})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e: 
        logger.error(f"Error creating access token: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
def decode_token(token: str) -> dict: 
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

async def get_current_user(authorization: str = Header(...)): 
    try: 
        token = authorization.split(" ")[1]
        payload = decode_token(token)
        return payload["sub"]
    
    except (JWTError, IndexError): 
        raise HTTPException(status_code=401, detail="Invalid credentials")