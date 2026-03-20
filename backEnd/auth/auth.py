
## There are 100 better ways to do auth than this.
## Don't do this
## I'm just being lazy


import logging
import os
from datetime import date
import json
import pymongo

from fastapi import Form, APIRouter, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager

from data.mongo import get_users_coll
from create.createTemplate import User

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
def login(credentials: Login): 

    try: 

        user = coll.find_one({"auth.username": credentials.username})
        if not user: 
            raise HTTPException(status_code=404, detail=f"User {credentials.username} not found.")
        
        if credentials.password != user['auth'].get('password'): 
            raise HTTPException(status_code=401, detail=f"Password is incorrect.")
        
        return user
    
    except Exception as e: 
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")