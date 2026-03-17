
from typing import Optional, List, Dict, Union
from typing_extensions import Literal
from pydantic import BaseModel

DeadliftType = Union[
    Literal[
        "Conventional",
        "Romanian",
        "Sumo", 
        "Single-Leg Romanian",
        "B-Stance",
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
    timestamp: str
    sets: int
    reps: int
    minWeight: Optional[float] = 0.0
    maxWeight: float
    allWeights: Optional[List[float]] = []
    amrap: Optional[Dict[str, Union[int, float]]] = {}
    pause: Optional[bool] = False
    estimatedRPE: Optional[float] = 0.0
    pr: Optional[bool] = False

class Deadlift(LiftInfo): 
    type: DeadliftType

class Press(LiftInfo): 
    type: Optional[PressType] = None

class Squat(LiftInfo): 
    type: Optional[SquatType] = None

class Cardio(BaseModel): 
    username: str
    timestamp: str
    type: CardioType
    distance: Optional[float] = 0.0
    hours: Optional[int] = 0
    minutes: Optional[int] = 0
    seconds: Optional[int] = 0

class Other(BaseModel): 
    username: str
    type: str
    timestamp: str
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