import pynvml

class NvidiaStats(object):
    def __init__(self):
        self._devices = defaultdict(pynvml.nvmlDeviceGetHandleByIndex)

    def device_count(self):
        return int(pynvml.nvmlDeviceGetCount())

    def device_name(self, index):
        return pynvml.nvmlDeviceGetName(self._devices[index])

    def gpu_temp(self, index):
        return int(pynvml.nvmlDeviceGetTemperature(self._devices[index], pynvml.NVML_TEMPERATURE_GPU))

    def device_fan_speed(self, index):
        """Fan speed as a percentage"""
        return int(pynvml.nvmlDeviceGetFanSpeed(self._devices[index]))

    def device_power_usage(self, index):
        """Power usage in milliwats"""
        return int(pynvml.nvmlDeviceGetPowerUsage(self._devices[index]))

    def device_power_limit(self, index):
        """Power management limit in milliwats"""
        return int(pynvml.nvmlDeviceGetPowerManagementLimit(self._devices[index]))

    def device_free_memory(self, index):
        return int(pynvml.nvmlDeviceGetMemoryInfo(self._devices[index]).free)

    def device_total_memory(self, index):
        return int(pynvml.nvmlDeviceGetMemoryInfo(self._devices[index]).total)

    def device_used_memory(self, index):
        return int(pynvml.nvmlDeviceGetMemoryInfo(self._devices[index]).used)

    def compute_processes(self, index):
        try:
            return len(pynvml.nvmlDeviceGetComputeRunningProcesses(self._devices[index]))
        except pynvml.NVMLError:
            return -1

    def graphics_processes(self, index):
        try:
            return len(pynvml.nvmlDeviceGetGraphicsRunningProcesses(self._devices[index]))
        except pynvml.NVMLError:
            return -1
