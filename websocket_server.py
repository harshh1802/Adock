import asyncio
import websockets

async def handler(websocket, path):
    async for message in websocket:
        print(f"Received: {message}")
        await websocket.send(f"Echo: {message}")

start_server = websockets.serve(handler, "localhost", 8081)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
