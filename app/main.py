from fastapi import FastAPI, WebSocket
from app.core.config import settings
from app.handlers.stream_receiver import stream_receiver
import asyncio
import aioredis

app = FastAPI()

# Initialize Redis client
@app.on_event("startup")
async def startup():
    app.state.redis = await aioredis.from_url(
        f"redis://{settings.redis.HOST}:{settings.redis.PORT}/{settings.redis.DB}"
    )

@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()

@app.websocket("/ws/stream")
async def stream_socket(websocket: WebSocket):
    redis_client = app.state.redis
    await stream_receiver(websocket=websocket, redis_client=redis_client)

