import subprocess, threading, queue

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
