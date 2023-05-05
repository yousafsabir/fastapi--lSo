from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Field
from typing import Optional
from datetime import datetime
from beanie import Document

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

# ------------ App's main logic ---------------
class Check(Document):
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    message: str


@app.on_event("startup")
async def connect_to_db():

    db = AsyncIOMotorClient("mongodb+srv://yousaf_project1:1214@cluster0.bzimi8z.mongodb.net/?retryWrites=true&w=majority").data

    await init_beanie(
        database=db,
        document_models=[
            Check
        ]
    )

    print("db connected")

@app.get("/{message}")
async def check_server(message: Optional[str] = None): 
    if message:
        check_in = Check(message=message)
        await check_in.save()
        return {
            "message": "Message Added",
	    "content": message
        }
    else:
        return {
            "message": "no message in request"
        }

@app.post("/{message}")
async def add_message(message: Optional[str] = None):
    if message:
        check_in = Check(message=message)
        await check_in.save()
        return {
            "message": "Message Added",
	    "content": message
        }
    else:
        return {
            "message": "no message in request"
        }
