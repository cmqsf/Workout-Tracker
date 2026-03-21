import functools
import os
from data.mongo import get_users_coll
from create.createTemplate import normalizeType
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

coll = get_users_coll()

def updateDLStats(createDeadlift): 

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
            
            blank_stats = {
                "numWorkouts": 0, 
                "pr": {
                    "conventional": 0.0,
                    "romanian": 0.0,
                    "sumo": 0.0,
                    "singleLegRomanian": 0.0,
                    "stiffLeg": 0.0,
                    "snatchGrip": 0.0,
                    "bStance": 0.0
                }
            }
            
            workoutStats = user.get('workoutStats')
            if not workoutStats: 
                workoutStats = {
                    "deadlifts": blank_stats
                }

            deadliftStats = workoutStats.get("numWorkouts")
            if not deadliftStats: 
                workoutStats['deadlifts'] = blank_stats
                deadliftStats = blank_stats

            currentNumWorkouts = deadliftStats.get('numWorkouts')
            if isinstance(currentNumWorkouts, int):
                update_fields["numWorkouts"] = currentNumWorkouts + 1

            dlType = normalizeType(request.type.split(" "))

            update_fields["pr"][dlType] = request.maxWeight           

        except Exception as e: 
            logger.error(f"Could not update user stats: {e}")