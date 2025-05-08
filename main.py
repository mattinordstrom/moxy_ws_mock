import asyncio
from websockets.asyncio.client import connect

port=9097

message = "Hello world!"
file="example" # Leave empty to use the default message above

async def send_message():
    global message
    uri = "ws://localhost:" + str(port) + "/moxywsmock"

    if file:
        with open("files/"+file, "r", encoding="utf-8") as f:
            message = f.read().strip()

    async with connect(uri) as websocket:
        await websocket.send(message)
        print(f"> Sent: {message}")


asyncio.run(send_message())
