import pynvml

def gpu_count():
    return int(pynvml.nvmlGetDeviceCount())
