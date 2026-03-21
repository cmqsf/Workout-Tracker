
from typing import Optional, List, Dict, Union
from typing_extensions import Literal
from pydantic import BaseModel
from datetime import date
import logging
from fastapi import HTTPException

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

DeadliftType = Union[
    Literal[
        "Conventional",
        "Romanian",
        "Sumo", 
        "Single Leg Romanian",
        "B Stance",
        "Stiff Leg",
        "Snatch Grip"
    ]
]

PressType = Union[
    Literal[
        "Barbell Bench",
        "Barbell Strict", 
        "Barbell Push",
        "Dumbbell Bench",
        "Dumbbell Strict",
        "Dumbbell Push"
    ]
]

SquatType = Union[
    Literal[
        "Back",
        "Front",
        "Single-Leg",
        "Goblet",
        "Hip Thrust"
    ]
]

CardioType = Union[
    Literal[
        "Run",
        "Walk", 
        "Hike",
        "Row"
    ]
]

class LiftInfo(BaseModel): 
    username: str
    day: int
    month: int
    year: int
    sets: int
    reps: int
    minWeight: Optional[float] = None
    maxWeight: float
    allWeights: Optional[List[float]] = []
    amrap: Optional[Dict[str, Union[int, float]]] = {}
    pause: Optional[bool] = False
    estimatedRPE: Optional[float] = None

class Deadlift(LiftInfo): 
    type: DeadliftType

class Press(LiftInfo): 
    type: Optional[PressType] = None

class Squat(LiftInfo): 
    type: Optional[SquatType] = None

class Cardio(BaseModel): 
    username: str
    day: int
    month: int
    year: int
    type: CardioType
    distance: Optional[float] = 0.0
    hours: Optional[int] = 0
    minutes: Optional[int] = 0
    seconds: Optional[int] = 0

class Other(BaseModel): 
    username: str
    type: str
    day: int
    month: int
    year: int
    details: Optional[str] = None
    weight: Optional[float] = 0.0
    sets: Optional[int] = 0
    reps: Optional[int] = 0

class User(BaseModel): 
    username: str
    fn: Optional[str] = None
    ln: Optional[str] = None
    birthYear: Optional[int] = None
    birthMonth: Optional[int] = None
    birthDay: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    email: Optional[str] = None
    password: Optional[str] = None

def populateWorkout(request: LiftInfo): 

    try: 
        
        timestamp = date(request.year, request.month, request.day)
        weights = {
            "minWeight": request.minWeight,
            "maxWeight": request.maxWeight,
            "allWeights": request.allWeights
        }

        if not request.minWeight: 
            del weights['minWeight']

        if not request.allWeights: 
            del weights['allWeights']
        
        workout = {
            "timestamp": str(timestamp),
            "sets": request.sets,
            "reps": request.reps,
            "weights": weights,
            "amrap": request.amrap,
            "pause": request.pause,
            "estimatedRPE": request.estimatedRPE
        }

        if not request.amrap: 
            del workout['amrap']

        if not request.estimatedRPE: 
            del workout['estimatedRPE']

        return workout

    except Exception as e: 
        logger.error(f"Error populating workout: {e}")

def determinePR(user: dict, type: str, maxWeight: float): 

    try: 
        user_stats = user.get("workoutStats")
        deadlift_stats = {}
        if user_stats: 
            deadlift_stats = user_stats.get("deadlifts", {})

        prs = []
        if deadlift_stats:
            prs = deadlift_stats.get("pr", [])

        pr = 0.0
        if prs and isinstance(prs, dict): 
            pr = prs.get(type.replace("-", "").replace(" ", "").lower(), 0.0)

        isPR = False
        if maxWeight > pr:
            isPR = True

        return isPR
    
    except Exception as e: 
        logger.error(f"Error determining PR: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def normalizeType(liftType: list) -> str: 

    try: 
        if len(liftType) == 1: 
            lt = liftType[0]
        else: 
            first = liftType[0]
            liftType.pop(0)
            if len(liftType) == 1: 
                lt = "".join(first + liftType[0].title())
            else:
                newLiftType = []
                for l in liftType: 
                    newLiftType.append(l.title())
                lt = "".join(first+"".join(newLiftType))  

        return lt

    except Exception as e: 
        logger.error(f"Error normalizing lift type.")
        return ""