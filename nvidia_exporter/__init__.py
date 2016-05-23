import pynvml

import .stats

if __name__ == '__main__':
    try:
        pynvml.nvmlInit()
        print(stats.gpu_count())
        pynvml.nvmlShutdown()
