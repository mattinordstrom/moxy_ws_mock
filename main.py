import asyncio
import argparse
from websockets.asyncio.client import connect

# python3 main.py -f "example2" -i 0

def parse_arguments():
    parser = argparse.ArgumentParser(description="MOXY WebSocket message sender.")
    parser.add_argument("-p", type=int, metavar="PORT", default=9097, help="Set the port (default: 9097)")
    parser.add_argument("-i", type=int, metavar="INTERVAL", default=3, help="Set the interval in seconds (default: 3). Set to 0 to send only once.")
    parser.add_argument("-m", type=str, metavar="MESSAGE", default="Hello world!", help="Message to send. (Will be used if file argument is not set.)")
    parser.add_argument("-f", type=str, metavar="FILE", default="", help="File name of a file in the /files path. (If set, file content will be used instead of the message argument.)")
    
    return parser.parse_args()


async def send_message(uri, message):
    async with connect(uri) as websocket:
        await websocket.send(message)
        print(f"> Sent: {message}")


async def main():
    args = parse_arguments()
    port = args.p
    interval = args.i
    message = args.m
    file = args.f

    uri = f"ws://localhost:{port}/moxywsmock"

    if file:
        with open(f"files/{file}", "r", encoding="utf-8") as f:
            message = f.read().strip()

    while True:
        await send_message(uri, message)
        if not interval or interval <= 0:
            break
        await asyncio.sleep(interval)

asyncio.run(main())
