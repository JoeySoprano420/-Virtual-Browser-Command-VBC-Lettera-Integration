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

