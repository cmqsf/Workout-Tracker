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

def updateStats(createDeadlift: F) -> F: 

    @functools.wraps(createDeadlift)
    def wrapper(*args, **kwargs): 
        try: 
            
            request = kwargs.get("request")
            if request is None: 
                logger.error("Could not find request.")
                return createDeadlift(*args, **kwargs)
            
            username = request.get("username", None)
            filter = {'auth.username': username}
            update_fields = {}
            user = coll.find_one(filter)
            if not user: 
                logger.error("Could not find user")
                return createDeadlift(*args, **kwargs)
            
            workoutStats = user.get('workoutStats')
            deadliftStats = workoutStats.get("numWorkouts")
            currentNumWorkouts = deadliftStats.get('numWorkouts', 0)

            if isinstance(currentNumWorkouts, int):
                update_fields["numWorkouts"] = currentNumWorkouts + 1

            dlType = normalizeType(request.type.split(" "))

            allPrs = deadliftStats.get("pr")
            if not allPrs: 
                pass
            pr = allPrs.get(dlType)
            if request.maxWeight > pr:
                update_fields["deadlifts"]["pr"][dlType] = request.maxWeight   

            coll.update_one(filter, {"$set": update_fields})
            logger.info("Successfully updated user stats!") 
            
            return createDeadlift(*args, **kwargs)                   

        except Exception as e: 
            logger.error(f"Could not update user stats: {e}")
            return createDeadlift(*args, **kwargs)

    return cast(F, wrapper)