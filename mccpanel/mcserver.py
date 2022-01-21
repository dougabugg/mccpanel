import subprocess, threading, time, bisect
from subprocess import PIPE

class PollPipe:
    def __init__(self, pipe, line_buffer_size=1024):
        self.pipe = pipe
        self.line_buffer_size = line_buffer_size
        self.poll_thread = threading.Thread(target=lambda: self.poll())
        self.line_buffer = []
        self.time_buffer = []
        self.poll_thread.start()

    def poll(self):
        for line in self.pipe:
            ts = int(time.time())
            self.line_buffer.append(line)
            self.time_buffer.append(ts)
            if len(self.line_buffer) > self.line_buffer_size * 2:
                self.line_buffer = self.line_buffer[-self.line_buffer_size:]
                self.time_buffer = self.time_buffer[-self.line_buffer_size:]

    def get_output(self, ts):
        i = bisect.bisect(self.time_buffer, ts)
        if len(self.time_buffer) > 0:
            last_ts = self.time_buffer[-1]
        else:
            last_ts = 0
        return {"lines": self.line_buffer[i:], "last_ts": last_ts}

class McServer:
    def __init__(self, name, jar_file, cwd, heap="4G"):
        self.name = name
        self.jar_file = jar_file
        self.cwd = cwd
        self.heap = heap
        self.proc = None
    def start(self):
        if self.proc != None and self.proc.poll() == None:
            return
        heap_max = self.heap
        heap_init = self.heap
        self.proc = subprocess.Popen(
            ["java", f"-Xmx{heap_max}", f"-Xms{heap_init}", "-jar", self.jar_file, "nogui"],
            stdin=PIPE, stdout=PIPE, # stderr=PIPE,
            cwd=self.cwd,
            text=True
        )
        self.poll_stdout = PollPipe(self.proc.stdout)
        # self.poll_stderr = PollPipe(self.proc.stderr)
    def force_stop(self):
        if self.proc != None:
            self.proc.terminate()
            self.poll_stdout = None
            # self.poll_stderr = None
    @property
    def pid(self):
        if self.proc is not None:
            if self.proc.poll() is not None:
                return self.proc.pid
        return None
    def is_running(self):
        if self.proc is None:
            return False
        if self.proc.poll() is None:
            return True
        return False
    def status(self):
        if self.proc == None:
            return "server not started yet"
        else:
            returncode = self.proc.poll()
            pid = self.proc.pid
            return f"[pid:{pid}] return code: {returncode}"
    def get_output(self, ts):
        if self.proc != None:
            return self.poll_stdout.get_output(ts)
        else:
            return {"lines": [], "last_ts": 0}
    def put_input(self, cmd):
        stdin = self.proc.stdin
        stdin.write(cmd + "\n")
        stdin.flush()