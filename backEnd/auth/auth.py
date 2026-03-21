
## There are 100 better ways to do auth than this.
## Don't do this
## I'm just being lazy


import logging
import os

from fastapi import Form, APIRouter, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager

from data.mongo import get_users_coll
from create.createTemplate import User
from auth.jwt import verify_password, create_access_token

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

coll = get_users_coll()

@asynccontextmanager
async def router_lifespan(app: APIRouter): 
    global schema
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yield

router = APIRouter(lifespan=router_lifespan)

class Login(BaseModel): 
    username: str
    password: str

@router.post("/login")
async def login(credentials: Login): 

    try: 

        user = coll.find_one({"auth.username": credentials.username})
        if not user: 
            raise HTTPException(status_code=404, detail=f"User {credentials.username} not found.")
        
        if not verify_password(credentials.password, user['auth'].get("password")): 
            raise HTTPException(status_code=401, detail="Incorrect password")
        
        token = create_access_token({"sub": credentials.username})

        return {"token": token}
    
    except HTTPException:
        raise
    
    except Exception as e: 
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")