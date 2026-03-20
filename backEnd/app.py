
import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from user.createUserProfile import router as createUser_route
from user.updateUserProfile import router as updateUser_route
from auth.auth import router as auth_route
from create.createDeadlift import router as deadlift_route
from create.createPress import router as press_route
from create.createSquat import router as squat_route

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "Content-Type"]
)

app.include_router(createUser_route)
app.include_router(updateUser_route)
app.include_router(auth_route)
app.include_router(deadlift_route)
app.include_router(press_route)
app.include_router(squat_route)

if __name__ == "__main__": 
    uvicorn.run(app, host='0.0.0.0', port=8000)
