import functools
from data.mongo import get_users_coll
from create.createTemplate import normalizeType
import logging
from typing import Callable, TypeVar, cast
from fastapi import Response

F = TypeVar("F", bound=Callable)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

coll = get_users_coll()

def updateDLStats(createPress: F) -> F: 

    @functools.wraps(createPress)
    def wrapper(*args, **kwargs): 
        try: 
            
            request = kwargs.get("request")
            if request is None: 
                logger.error("Could not find request.")
                return createPress(*args, **kwargs)
            
            username = request.get("username", None)
            filter = {'auth.username': username}
            update_fields = {}
            user = coll.find_one(filter)
            if not user: 
                logger.error("Could not find user")
                return createPress(*args, **kwargs)
            
            workoutStats = user.get('workoutStats')
            if not workoutStats: 
                pass

            pressStats = workoutStats.get("numWorkouts")
            if not pressStats: 
                pass

            currentNumWorkouts = pressStats.get('numWorkouts', 0)
            if isinstance(currentNumWorkouts, int):
                update_fields["numWorkouts"] = currentNumWorkouts + 1

            pressType = normalizeType(request.type.split(" "))

            allPrs = pressStats.get("pr")
            if not allPrs: 
                pass
            pr = allPrs.get(pressType)
            if request.maxWeight > pr:
                update_fields["press"]["pr"][pressType] = request.maxWeight   

            coll.update_one(filter, {"$set": update_fields})
            logger.info("Successfully updated user stats!") 
            
            return createPress(*args, **kwargs)                   

        except Exception as e: 
            logger.error(f"Could not update user stats: {e}")
            return createPress(*args, **kwargs)

    return cast(F, wrapper)