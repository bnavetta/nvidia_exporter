import pynvml

class NvidiaStats(object):
    def __init__(self):
        self._devices = dict()

    def _device(self, index):
        if index in self._devices:
            return self._devices[index]
        else:
            handle = pynvml.nvmlDeviceGetHandleByIndex(index)
            self._devices[index] = handle
            return handle

    def device_count(self):
        return int(pynvml.nvmlDeviceGetCount())

    def device_name(self, index):
        return pynvml.nvmlDeviceGetName(self._device(index))

    def gpu_temp(self, index):
        return int(pynvml.nvmlDeviceGetTemperature(self._device(index), pynvml.NVML_TEMPERATURE_GPU))

    def device_fan_speed(self, index):
        """Fan speed as a percentage"""
        return int(pynvml.nvmlDeviceGetFanSpeed(self._device(index)))

    def device_power_usage(self, index):
        """Power usage in milliwats"""
	try:
            return int(pynvml.nvmlDeviceGetPowerUsage(self._device(index)))
        except pynvml.NVMLError:
            return -1

    def device_power_limit(self, index):
        """Power management limit in milliwats"""
        try:
            return int(pynvml.nvmlDeviceGetPowerManagementLimit(self._device(index)))
        except pynvml.NVMLError:
            return -1

    def device_free_memory(self, index):
        return int(pynvml.nvmlDeviceGetMemoryInfo(self._device(index)).free)

    def device_total_memory(self, index):
        return int(pynvml.nvmlDeviceGetMemoryInfo(self._device(index)).total)

    def device_used_memory(self, index):
        return int(pynvml.nvmlDeviceGetMemoryInfo(self._device(index)).used)

    def compute_processes(self, index):
        try:
            return len(pynvml.nvmlDeviceGetComputeRunningProcesses(self._device(index)))
        except pynvml.NVMLError:
            return -1

    def graphics_processes(self, index):
        try:
            return len(pynvml.nvmlDeviceGetGraphicsRunningProcesses(self._device(index)))
        except pynvml.NVMLError:
            return -1
