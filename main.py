import os
import sys
import asyncio
import argparse
from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosed, InvalidHandshake, InvalidURI

YELLOW = '\033[93m'
ENDC = '\033[0m'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def parse_arguments():
    parser = argparse.ArgumentParser(description="MOXY WebSocket message sender.")
    parser.add_argument("-p", type=int, metavar="PORT", default=9097, help="Set the port (default: 9097)")
    parser.add_argument("-i", type=int, metavar="INTERVAL", default=3000, help="Set the interval in milliseconds (default: 3000). Set to 0 to send only once.")
    parser.add_argument("-m", type=str, metavar="MESSAGE", default="Hello world!", help="Message to send. (Will be used if file argument is not set.)")
    parser.add_argument("-f", type=str, metavar="FILE", default="", help="File name of a file in the /files path. For .jsonl files, each line is sent separately. For .json files, the entire content is sent as one message.")
    parser.add_argument("-l", action="store_true", help="List available files in the /files directory.")
    
    return parser.parse_args()


async def discard_incoming(websocket):
    try:
        async for _ in websocket:
            pass
    except ConnectionClosed:
        pass


async def send_messages(uri, messages, interval, file):
    try:
        async with connect(uri) as websocket:
            # moxy echoes every message back; unread echoes fill the queue and stall keepalive pongs
            reader = asyncio.create_task(discard_incoming(websocket))  # noqa: F841 keep a reference so the task isn't garbage collected

            if file:
                for message in messages:
                    await websocket.send(message)
                    print(f"\n{YELLOW}Sent:{ENDC} {message}")

                    if interval and interval > 0:
                        await asyncio.sleep(interval)

                return 0

            while True:
                await websocket.send(messages[0])
                print(f"\n{YELLOW}Sent:{ENDC} {messages[0]}")

                if not interval or interval <= 0:
                    break
                await asyncio.sleep(interval)
    except (OSError, InvalidHandshake, InvalidURI) as e:
        print(f"Error when connecting to moxy at {uri}. Is the server running? ({e})")
        return 1
    except ConnectionClosed as e:
        print(f"Connection to moxy at {uri} was closed: {e}")
        return 1

    return 0


async def main():
    args = parse_arguments()
    port = args.p
    interval = args.i / 1000  # Convert milliseconds to seconds
    message = args.m
    file = args.f

    if args.l:
        files = os.listdir(os.path.join(BASE_DIR, "files"))
        print("Available files:")
        for f in files:
            print(f"- {f}")
        print("\n")
        return 0

    uri = f"ws://localhost:{port}/moxywsmock"

    if file:
        file_path = os.path.join(BASE_DIR, "files", file)

        if not os.path.isfile(file_path):
            print(f"File not found: {file}. Use -l to list available files.")
            return 1

        # Check if it's a JSON file (not JSONL)
        if file.endswith('.json'):
            with open(file_path, "r", encoding="utf-8") as f:
                # Read entire JSON file as a single message
                json_content = f.read().strip()
                messages = [json_content] if json_content else []
        else:
            # Handle JSONL files (line by line)
            with open(file_path, "r", encoding="utf-8") as f:
                messages = [line.strip() for line in f if line.strip()]
        if not messages:
            print(f"File is empty: {file}")
            return 1
    else:
        messages = [message]

    if len(messages) > 1 and (not interval or interval <= 0):
        print("Interval can not be 0 for files with multiple rows.")
        return 1

    return await send_messages(uri, messages, interval, file)


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
        sys.exit(130)
