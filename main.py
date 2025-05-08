import asyncio
from websockets.asyncio.client import connect

port=9097

interval = 3  # Set interval in seconds (set to None or 0 to disable repeated calls)

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


async def main():
    while True:
        await send_message()
        if not interval or interval <= 0:
            break
        await asyncio.sleep(interval)

asyncio.run(main())
