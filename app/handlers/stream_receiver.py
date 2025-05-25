from fastapi import WebSocket, WebSocketDisconnect
import redis.asyncio as redis
from app.libs.api_sigasiga_rest import ApiSigaSigaRest

async def stream_receiver(websocket: WebSocket, redis_client: redis.Redis):
    await websocket.accept()
    # ws_id = websocket._headers.get("sec-websocket-key")
    api_sigasiga_rest = ApiSigaSigaRest()
    query_params = websocket.query_params
    event_id = query_params.get("eventId")
    token = query_params.get("token")
    client_id = query_params.get("clientId")
    ws_id = client_id
    valid_client = await api_sigasiga_rest.validate_and_start_client(token, ws_id)
    client_input_video_buffer = f"{event_id}-chunks_data_input_buffer-{ws_id}"

    if not valid_client:
        print(f"🔌 Cliente no autorizado para el stream! {str(websocket)}")
        await websocket.close(code=1008)
        return
    try:
        print(f"📺 Streaming iniciado: Cliente {str(websocket)} - Evento {event_id}")
        while True:
            data = await websocket.receive_bytes()
            await redis_client.rpush(client_input_video_buffer, data)

    except WebSocketDisconnect:
        disconnect_status = await api_sigasiga_rest.disconnect_client(token, ws_id)
        print(f"🔌 Cliente desconectado del stream {ws_id}. Evento {event_id}. Status: {disconnect_status}")