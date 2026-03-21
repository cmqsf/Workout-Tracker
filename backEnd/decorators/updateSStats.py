import functools
from data.mongo import get_users_coll
from create.createTemplate import normalizeType
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

coll = get_users_coll()

def updateDLStats(createSquat): 

    @functools.wraps(createSquat)
    def wrapper(*args, **kwargs): 
        try: 
            
            request = kwargs.get("request")
            if request is None: 
                logger.error("Could not find request.")
                return createSquat(*args, **kwargs)
            
            username = request.get("username", None)
            filter = {'auth.username': username}
            update_fields = {}
            user = coll.find_one(filter)
            if not user: 
                logger.error("Could not find user")
                return createSquat(*args, **kwargs)
            
            workoutStats = user.get('workoutStats')
            if not workoutStats: 
                pass

            squatStats = workoutStats.get("numWorkouts")
            if not squatStats: 
                pass

            currentNumWorkouts = squatStats.get('numWorkouts', 0)
            if isinstance(currentNumWorkouts, int):
                update_fields["numWorkouts"] = currentNumWorkouts + 1

            squatType = normalizeType(request.type.split(" "))

            allPrs = squatStats.get("pr")
            if not allPrs: 
                pass
            pr = allPrs.get(squatType)
            if request.maxWeight > pr:
                update_fields["squats"]["pr"][squatType] = request.maxWeight   

            coll.update_one(filter, {"$set": update_fields})
            logger.info("Successfully updated user stats!") 
            
            return createSquat(*args, **kwargs)                   

        except Exception as e: 
            logger.error(f"Could not update user stats: {e}")

        return wrapper