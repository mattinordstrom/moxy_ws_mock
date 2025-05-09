import os
import asyncio
import argparse
from websockets.asyncio.client import connect

# python3 main.py -f "example2" -i 0

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def parse_arguments():
    parser = argparse.ArgumentParser(description="MOXY WebSocket message sender.")
    parser.add_argument("-p", type=int, metavar="PORT", default=9097, help="Set the port (default: 9097)")
    parser.add_argument("-i", type=int, metavar="INTERVAL", default=3000, help="Set the interval in milliseconds (default: 3000). Set to 0 to send only once.")
    parser.add_argument("-m", type=str, metavar="MESSAGE", default="Hello world!", help="Message to send. (Will be used if file argument is not set.)")
    parser.add_argument("-f", type=str, metavar="FILE", default="", help="File name of a file in the /files path. (If set, file content will be used instead of the message argument.) Each row will be sent as a separate message with the interval set until all rows has been processed.")
    parser.add_argument("-l", action="store_true", help="List available files in the /files directory.")
    
    return parser.parse_args()


async def send_messages(uri, messages, interval, file):
    try:
        async with connect(uri) as websocket:
            if file:
                for message in messages:
                    await websocket.send(message)
                    print(f"[Sent] {message}")

                    if interval and interval > 0:
                        await asyncio.sleep(interval)
                        
                return

            while True:
                await websocket.send(messages[0])
                print(f"[Sent] {messages[0]}")

                if not interval or interval <= 0:
                    break
                await asyncio.sleep(interval)
    except Exception as e:
        print(f"Error when connecting to moxy at {uri}. Is the server running?")
    

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
        return
    
    uri = f"ws://localhost:{port}/moxywsmock"

    if file:
        file_path = os.path.join(BASE_DIR, "files", file)
        with open(file_path, "r", encoding="utf-8") as f:
            messages = [line.strip() for line in f if line.strip()]
    else:
        messages = [message]

    if len(messages) > 1 and (not interval or interval <= 0):
        print("Interval can not be 0 for files with multiple rows.")
        return
                  
    await send_messages(uri, messages, interval, file)
  

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
