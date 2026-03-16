
import logging
import os
from datetime import date
import json

from fastapi import Form, APIRouter, HTTPException
from typing import Annotated
from contextlib import asynccontextmanager

from data.mongo import get_users_coll
from create.createTemplate import NewUser

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

try: 
    users_db = os.environ["MONGO_USERS_DB"]
except Exception as e: 
    logger.error(f"Error loading env variables: {e}")

users = get_users_coll()

@asynccontextmanager
async def router_lifespan(app: APIRouter): 
    global schema
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yield

router = APIRouter(lifespan=router_lifespan)

def populateUser(model): 

    try: 

        age = date.today().year - model.birthYear
        birthday = model.birthYear
        if model.birthMonth and model.birthDay:
            birthday = f"{model.birthDay}.{model.birthMonth}.{model.birthYear}"

        bmi = None
        if model.weight and model.height: 
            bmi = (model.weight/(model.height*model.height))
        
        user = {
            "basicInfo": {
                "fn": model.fn,
                "ln": model.ln,
                "age": age,
                "birthday": birthday,
                "weight": model.weight,
                "height": model.height,
                "bmi": bmi
            }
        }

    except Exception as e: 
        logger.error(f"Error in populateUser: {e}")

@router.post("/create-user")
async def create(request: Annotated[str, Form()]): 

    try: 
        model = json.loads(request)
        model = NewUser(**model)

    except HTTPException: 
        raise

    except Exception as e: 
        logger.error(e)
        raise HTTPException(status_code = 500, detail = "Internal Server Error")