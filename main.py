import asyncio
from websockets.asyncio.client import connect

port=9097

async def send_message():
    uri = "ws://localhost:" + str(port) + "/moxywsmock"

    async with connect(uri) as websocket:
        message = "Hello world!"
        await websocket.send(message)
        print(f"> Sent: {message}")

asyncio.run(send_message())
