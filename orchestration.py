import subprocess, threading, queue, threading, queue, asyncio

class VBCProcess:
    def __init__(self, path):
        self.path = path
        self.q = queue.Queue()
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while True:
            msg = self.q.get()
            if msg == "STOP": break
            result = subprocess.run(["python", "main.py", self.path], input=msg.encode(), capture_output=True)
            print(f"[{self.path} reply]: {result.stdout.decode()}")

    def send(self, msg):
        self.q.put(msg)

def broadcast(processes, msg):
    for p in processes:
        p.send(msg)

channels = {}

def run_channel(name):
    channels[name] = queue.Queue()

def send(ch, val):
    channels[ch].put(val)

def receive(ch):
    return channels[ch].get()

def spawn(func, *args):
    t = threading.Thread(target=func, args=args)
    t.start()
    return t

async def async_task(coro):
    return await coro

class VBCProcess:
    def __init__(self, path):
        self.path = path
        self.vars = {}
        self.q = queue.Queue()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

import socket, threading, json

def start_listener(port, handler):
    def server():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", port))
        s.listen()
        print(f"[VBC] Listening on {port}")
        while True:
            conn, addr = s.accept()
            data = conn.recv(4096)
            if not data: break
            msg = json.loads(data.decode())
            handler(msg, addr)
            conn.close()
    threading.Thread(target=server, daemon=True).start()

def send_message(host, port, msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(json.dumps(msg).encode())
    s.close()

import asyncio, websockets, json

clients = set()

async def handler(ws):
    clients.add(ws)
    try:
        async for msg in ws:
            for c in clients:
                if c != ws:
                    await c.send(msg)
    finally:
        clients.remove(ws)

async def server():
    async with websockets.serve(handler,"0.0.0.0",8765):
        await asyncio.Future()  # run forever

