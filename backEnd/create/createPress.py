
import logging
import os
from datetime import date

from fastapi import APIRouter, HTTPException
from contextlib import asynccontextmanager

from data.mongo import get_collection, get_users_coll
from create.createTemplate import *

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

try: 
    coll_name = os.environ["DEADLIFT_COLL_NAME"]
except Exception as e: 
    logger.error(f"Error loading params: {e}")

users = get_users_coll()

@asynccontextmanager
async def router_lifespan(app: APIRouter): 
    global schema
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yield

router = APIRouter(lifespan=router_lifespan)

@router.post("/squat")
def createSquat(request: Press): 
    try: 
        liftInfo = LiftInfo(**request.model_dump(exclude={'type'}))
        workout = populateWorkout(liftInfo)
        user = users.find_one({'auth.username': request.username})

        ## Avoiding those annoying squiggly lines
        if workout is None: 
            return HTTPException(status_code=500, detail=f"Internal Server Error: workout not created")
        
        if user is None: 
            raise HTTPException(status_code=404, detail="User not found")
        
        workout['type'] = request.type
        workout['pr'] = determinePR(user, str(request.type), request.maxWeight)

        coll = get_collection(request.username, coll_name)
        coll.insert_one(workout)

        return "Successfully entered workout!"
    
    except Exception as e: 
        logger.error(f"Error creating press workout: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
