import pynvml

class NvidiaStats:
    def gpu_count(self):
        return int(pynvml.nvmlDeviceGetCount())

# running processes, GPU temp, memory usage, GPU speed?

devicegetcomputrunningprocesses and devicegetgraphicsrunningprocesses
