from pynvml import *
from prometheus_client import Gauge

from .metric import Metric


def register_standard_metrics():
    Gauge('nvidia_device_count', 'Number of compute devices in the system')\
        .set_function(lambda: int(nvmlDeviceGetCount()))

    metrics = [
        Metric('gpu_temp_degC',
               'GPU Temperature (in degrees Celsius)',
               lambda h: nvmlDeviceGetTemperature(h, NVML_TEMPERATURE_GPU)),
        Metric('mem_total_bytes',
               'Total installed FB memory (in  bytes)',
               lambda h: nvmlDeviceGetMemoryInfo(h).total),
        Metric('mem_free_bytes',
               'Unallocated FB memory (in bytes)',
               lambda h: nvmlDeviceGetMemoryInfo(h).free),
        Metric('mem_used_bytes',
               'Allocated FB memory (in bytes)',
               lambda h: nvmlDeviceGetMemoryInfo(h).used),
        Metric('shutdown_temp_degC',
               'Shutdown temperature threshold (in degrees Celsius)',
               lambda h: nvmlDeviceGetTemperatureThreshold(h, 0)),
        Metric('slowdown_temp_degC',
               'Slowdown temperature threshold (in degrees Celsius)',
               lambda h: nvmlDeviceGetTemperatureThreshold(h, 1)),
        Metric('process_count',
               'Number of running compute processes',
               lambda h: len(nvmlDeviceGetComputeRunningProcesses(h)))
    ]

    device_count = int(nvmlDeviceGetCount())
    for device_index in range(device_count):
        handle = nvmlDeviceGetHandleByIndex(device_index)
        name = nvmlDeviceGetName(handle)

        for metric in metrics:
            metric.metric_for(name, device_index, handle)