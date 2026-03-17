
import logging
import os
from datetime import date

from fastapi import APIRouter, HTTPException
from contextlib import asynccontextmanager

from data.mongo import get_collection, get_users_coll
from create.createTemplate import DeadliftType, Deadlift, populateWorkout, LiftInfo

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

@router.post("/deadlift")
def createDeadlift(request: Deadlift): 
    try: 
        liftInfo = LiftInfo(**request.model_dump(exclude={'type'}))
        workout = populateWorkout(liftInfo)
        if workout is None: 
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
        workout['type'] = request.type

        user = users.find_one({"auth.username": request.username})
        if user is None: 
            raise HTTPException(status_code=404, detail="User not found")
        
        user_stats = user.get("workoutStats")
        if user_stats: 
            deadlift_stats = user_stats.get("deadlifts", {})

        if deadlift_stats: 
            prs = deadlift_stats.get("pr", [])

        if prs and isinstance(prs, dict): 
            pr = prs.get(request.type.replace("-", "").replace(" ", "").lower(), 0.0)

        workout['pr'] = False
        if request.maxWeight > pr: 
            workout['pr'] = True

        coll = get_collection(request.username, coll_name)
        coll.insert_one(workout)

        return "Successfully entered workout!"

    except Exception as e: 
        logger.error(f"Error populating deadlift workout: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")