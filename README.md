# moxy ws mock

## Purpose

This can be used to send websocket messages to moxy. https://github.com/mattinordstrom/moxy    
  
    
## Setup

Create a virtual env:

    python3 -m venv .moxy_ws_venv

Activate it:

    source .moxy_ws_venv/bin/activate

Install requirements:

    pip3 install -r requirements.txt


## Help

    python3 main.py --help


## Simple run

    python3 main.py -i 0


## Add alias

Add to ~/.zshrc:

    alias moxyws="/home/matti/projects/moxy_ws_mock/.moxy_ws_venv/bin/python3 /home/matti/projects/moxy_ws_mock/main.py "$1

then you can just run:

    moxyws -i 0