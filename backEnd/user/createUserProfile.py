
import logging
import os
from datetime import date

from fastapi import APIRouter, HTTPException
from contextlib import asynccontextmanager

from auth.jwt import hash_password

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

def checkUserExists(username): 

    if coll.find_one({"auth.username": username}): 
        return True
    
    return False

def populateUser(request): 

    try: 

        age = ((date.today() - date(request.birthYear, request.birthMonth, request.birthDay)).days)//365.25
        birthday = request.birthYear
        if request.birthMonth and request.birthDay:
            birthday = f"{request.birthDay}.{request.birthMonth}.{request.birthYear}"

        bmi = None
        if request.weight and request.height: 
            bmi = (request.weight/(request.height*request.height))
        
        user = {
            "basicInfo": {
                "fn": request.fn,
                "ln": request.ln,
                "age": int(age),
                "birthday": birthday,
                "weight": request.weight,
                "height": request.height,
                "bmi": bmi
            },
            "auth": {
                "username": request.username,
                "email": request.email,
                "password": hash_password(request.password)
            }
        }
        return user

    except Exception as e: 
        logger.error(f"Error in populateUser: {e}")

@router.post("/create-user")
async def create(request: User): 

    if checkUserExists(request.username): 
        return "User already exists!"

    try: 
        
        user = populateUser(request)
        result = coll.insert_one(user)
        if result: 
            return "Successfully inserted document!"

    except HTTPException: 
        raise

    except Exception as e: 
        logger.error(e)
        raise HTTPException(status_code = 500, detail = "Internal Server Error")