from prometheus_client import Gague
from pynvml import *

DEVICE_INDEX_LABEL = 'device_index'
DEVICE_NAME_LABEL = 'device_name'
DRIVER_VERSION_LABEL = 'driver_version'

class Metric(object):
    __slots__ = ['name', 'description', '_prometheus_metric']

    def collect(self, handle):
        raise NotImplementedError("Must be overridden by subclass")

    @property
    def promethus_metric(self):
        # TODO: support non-gague metrics
        if not self._prometheus_metric:
            self._prometheus_metric = Gague('nvidia_' + self.name, self.description, [DEVICE_INDEX_LABEL, DEVICE_NAME_LABEL, DRIVER_VERSION_LABEL])
        return self._prometheus_metric

class TemperatureMetric(Metric):
    def __init__(self):
        self.name = 'gpu_temp_degC'
        self.description = 'GPU Temperature (in degrees Celsius)'

    def collect(self, handle):
        return nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)

class TotalMemoryMetric(Metric):
    def __init__(self):
        self.name = 'mem_total_bytes'
        self.description = 'Total installed FB memory (in  bytes)'

    def collect(self, handle):
        return nvmlDeviceGetMemoryInfo(handle).total

class FreeMemoryMetric(Metric):
    def __init__(self):
        self.name = 'mem_free_bytes'
        self.description = 'Unallocated FB memory (in bytes)'

    def collect(self, handle):
        return nvmlDeviceGetMemoryInfo(handle).free

class UsedMemoryMetric(Metric):
    def __init__(self):
        self.name = 'mem_used_bytes'
        self.description = 'Allocated FB memory (in bytes)'

    def collect(self, handle):
        return nvmlDeviceGetMemoryInfo(handle).used

class GPUUtilizationMetric(Metric):
    def __init__(self):
        self.name = 'gpu_util'
        self.description = 'Percent of time over the past sample period during which one or more kernels was executing on the GPU'

    def collect(self, handle):
        return nvmlDeviceGetUtilizationRates(handle).gpu

class MemoryUtilizationMetric(Metric):
    def __init__(self):
        self.name = 'mem_util'
        self.description = 'Percent of time over the past sample period during which global (device) memory was being read or written'

    def collect(self, handle):
        return nvmlDeviceGetUtilizationRates(handle).memory

class FanSpeedMetric(Metric):
    def __init__(self):
        self.name = 'fan_speed'
        self.description = 'Fan speed as a percent of the maximum, assuming the fan is not physically blocked'

    def collect(self):
        try:
            return nvmlDeviceGetFanSpeed(handle)
        except NVMLError, nvmlError:
            # Some GPUs don't have fans
            if nvmlError.value == NVML_ERROR_NOT_SUPPORTED:
                return 0

class PowerUsageMetric(Metric):
    def __init__(self):
        self.name = 'power_usage_W'
        self.description = 'Power usage in watts for the GPU and associated circuitry (e.g. memory)'

    def collect(self, handle):
        return nvmlDeviceGetPowerUsage(handle) / 1000

class PowerManagementLimitMetric(Metric):
    def __init__(self):
        self.name = 'power_management_limit_W'
        self.description = 'Upper limit for power draw at which the power management algorithm kicks in (in watts)'

    def collect(self, handle):
        return nvmlDeviceGetPowerManagementLimit(handle) / 1000

class ECCDoubleBitErrorsMetric(Metric):
    def __init__(self):
        self.name = 'ecc_db_errors'
        self.description = 'Count of double-bit (uncorrected) ECC errors over the lifetime of the device'

    def collect(self, handle):
        return nvmlDeviceGetTotalEccErrors(handle, 1, 1)

class ECCSingleBitErrorsMetric(Metric):
    def __init__(self):
        self.name = 'ecc_sb_errors'
        self.description = 'Count of single-bit (corrected) ECC errors over the lifetime of the device'

    def collect(self, handle):
        return nvmlDeviceGetTotalEccErrors(handle, 0, 1)

class ShutdownTemperatureMetric(Metric):
    def __init__(self):
        self.name = 'shutdown_temperature_degC'
        self.description = 'Shutdown temperature threshold (in degrees Celsius)'

    def collect(self, handle):
        return nvmlDeviceGetTemperatureThreshold(handle, 0)

class SlowdownTemperatureMetric(Metric):
    def __init__(self):
        self.name = 'slowdown_temperature_degC'
        self.description = 'Slowdown temperature threshold (in degrees Celsius)'

    def collect(self, handle):
        return nvmlDeviceGetTemperatureThreshold(handle, 1)

class ProcessCountMetric(Metric):
    def __init__(self):
        self.name = 'process_count'
        self.description = 'Number of running compute processes'

    def collect(self, handle):
        return nvmlDeviceGetComputeRunningProcesses(handle)
