import pynvml

from . import stats

if __name__ == '__main__':
    try:
        pynvml.nvmlInit()
        print(stats.gpu_count())
        pynvml.nvmlShutdown()
    except pynvml.NVMLError, err:
        print("NVML error: %s" % err)
