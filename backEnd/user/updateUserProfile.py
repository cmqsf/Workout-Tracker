
import logging
import os
from datetime import date
import json
import pymongo
import requests

from fastapi import Form, APIRouter, HTTPException
from typing import Annotated
from contextlib import asynccontextmanager

from data.mongo import get_users_coll
from create.createTemplate import User
from user.createUserProfile import populateUser

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

try: 
    users_db = os.environ["MONGO_USERS_DB_NAME"]
except Exception as e: 
    logger.error(f"Error loading env variables: {e}")

coll = get_users_coll()

@asynccontextmanager
async def router_lifespan(app: APIRouter): 
    global schema
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yield

router = APIRouter(lifespan=router_lifespan)

@router.put("/update-user/{username}")
async def update(username: str, request: User):
    
    try: 

        user = populateUser(request)
        old_stats = coll.find_one({"auth.username": username})
        if user and old_stats:  
            user['workoutStats'] = old_stats.get("workoutStats")

        result = coll.update_one({"auth.username": username}, {"$set": user})

        if result: 
            return "Successfully updated document!"

    except Exception as e: 
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")