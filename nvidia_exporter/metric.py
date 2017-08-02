import functools
from prometheus_client import Gauge
from pynvml import *

DEVICE_INDEX_LABEL = 'device_index'
DEVICE_NAME_LABEL = 'device_name'
DRIVER_VERSION_LABEL = 'driver_version'

class Metric(object):
    __slots__ = ['name', 'description', 'prometheus_metric']

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.prometheus_metric = Gauge('nvidia_' + name, description, [DEVICE_INDEX_LABEL, DEVICE_NAME_LABEL, DRIVER_VERSION_LABEL])

    def collect(self, handle):
        raise NotImplementedError("Must be overridden by subclass")

    def collect_fn(self, handle):
        return functools.partial(self.collect, handle)

class TemperatureMetric(Metric):
    def __init__(self):
        super(TemperatureMetric, self).__init__(
            'gpu_temp_degC',
            'GPU Temperature (in degrees Celsius)'
        )

    def collect(self, handle):
        return nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)

class TotalMemoryMetric(Metric):
    def __init__(self):
        super(TotalMemoryMetric, self).__init__(
            'mem_total_bytes',
            'Total installed FB memory (in  bytes)'
        )

    def collect(self, handle):
        return nvmlDeviceGetMemoryInfo(handle).total

class FreeMemoryMetric(Metric):
    def __init__(self):
        super(FreeMemoryMetric, self).__init__(
            'mem_free_bytes',
            'Unallocated FB memory (in bytes)'
        )

    def collect(self, handle):
        return nvmlDeviceGetMemoryInfo(handle).free

class UsedMemoryMetric(Metric):
    def __init__(self):
        super(UsedMemoryMetric, self).__init__(
            'mem_used_bytes',
            'Allocated FB memory (in bytes)'
        )

    def collect(self, handle):
        return nvmlDeviceGetMemoryInfo(handle).used

class GPUUtilizationMetric(Metric):
    def __init__(self):
        super(GPUUtilizationMetric, self).__init__(
            'gpu_util',
            'Percent of time over the past sample period during which one or more kernels was executing on the GPU'
        )

    def collect(self, handle):
        return nvmlDeviceGetUtilizationRates(handle).gpu

class MemoryUtilizationMetric(Metric):
    def __init__(self):
        super(MemoryUtilizationMetric, self).__init__(
            'mem_util',
            'Percent of time over the past sample period during which global (device) memory was being read or written'
        )

    def collect(self, handle):
        return nvmlDeviceGetUtilizationRates(handle).memory

class FanSpeedMetric(Metric):
    def __init__(self):
        super(FanSpeedMetric, self).__init__(
            'fan_speed',
            'Fan speed as a percent of the maximum, assuming the fan is not physically blocked'
        )

    def collect(self, handle):
        try:
            return nvmlDeviceGetFanSpeed(handle)
        except NVMLError, nvmlError:
            # Some GPUs don't have fans
            if nvmlError.value == NVML_ERROR_NOT_SUPPORTED:
                return 0

class PowerUsageMetric(Metric):
    def __init__(self):
        super(PowerUsageMetric, self).__init__(
            'power_usage_W',
            'Power usage in watts for the GPU and associated circuitry (e.g. memory)'
        )

    def collect(self, handle):
        return nvmlDeviceGetPowerUsage(handle) / 1000

class PowerManagementLimitMetric(Metric):
    def __init__(self):
        super(PowerManagementLimitMetric, self).__init__(
            'power_management_limit_W',
            'Upper limit for power draw at which the power management algorithm kicks in (in watts)'
        )

    def collect(self, handle):
        return nvmlDeviceGetPowerManagementLimit(handle) / 1000

class ECCDoubleBitErrorsMetric(Metric):
    def __init__(self):
        super(ECCDoubleBitErrorsMetric, self).__init__(
            'ecc_db_errors',
            'Count of double-bit (uncorrected) ECC errors over the lifetime of the device'
        )

    def collect(self, handle):
        return nvmlDeviceGetTotalEccErrors(handle, 1, 1)

class ECCSingleBitErrorsMetric(Metric):
    def __init__(self):
        super(ECCSingleBitErrorsMetric, self).__init__(
            'ecc_sb_errors',
            'Count of single-bit (corrected) ECC errors over the lifetime of the device'
        )

    def collect(self, handle):
        return nvmlDeviceGetTotalEccErrors(handle, 0, 1)

class ShutdownTemperatureMetric(Metric):
    def __init__(self):
        super(ShutdownTemperatureMetric, self).__init__(
            'shutdown_temperature_degC',
            'Shutdown temperature threshold (in degrees Celsius)'
        )

    def collect(self, handle):
        return nvmlDeviceGetTemperatureThreshold(handle, 0)

class SlowdownTemperatureMetric(Metric):
    def __init__(self):
        super(SlowdownTemperatureMetric, self).__init__(
            'slowdown_temperature_degC',
            'Slowdown temperature threshold (in degrees Celsius)'
        )

    def collect(self, handle):
        return nvmlDeviceGetTemperatureThreshold(handle, 1)

class ProcessCountMetric(Metric):
    def __init__(self):
        super(ProcessCountMetric, self).__init__(
            'process_count',
            'Number of running compute processes'
        )

    def collect(self, handle):
        return len(nvmlDeviceGetComputeRunningProcesses(handle))
