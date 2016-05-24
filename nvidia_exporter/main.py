import pynvml

from .stats import NvidiaStats

if __name__ == '__main__':
    try:
        pynvml.nvmlInit()
        stats = NvidiaStats()
        for device_index in range(0, stats.device_count()):
            print("Device name", stats.device_name(device_index))
            print("GPU temperature", stats.gpu_temp(device_index))
            print("Fan speed", stats.device_fan_speed(device_index))
            print("Power usage", stats.device_power_usage(device_index))
            print("Power limit", stats.device_power_limit(device_index))
            print("Free memory", stats.device_free_memory(device_index))
            print("Used memory", stats.device_used_memory(device_index))
            print("Total memory", stats.device_total_memory(device_index))
            print("Graphics processes", stats.graphics_processes(device_index))
            print("Compute processes", stats.compute_processes(device_index))
        pynvml.nvmlShutdown()
    except pynvml.NVMLError, err:
        print("NVML error: %s" % err)
