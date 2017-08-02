from pynvml import *
from prometheus_client import Gauge

from .metric import *

def build_metrics():
    metrics = [
        TemperatureMetric(), ShutdownTemperatureMetric(), SlowdownTemperatureMetric(), FanSpeedMetric(),
        TotalMemoryMetric(), FreeMemoryMetric(), UsedMemoryMetric(),
        GPUUtilizationMetric(), MemoryUtilizationMetric(),
        PowerUsageMetric(), PowerManagementLimitMetric(),
        # ECCDoubleBitErrorsMetric(), ECCSingleBitErrorsMetric(), # doesn't seem to be supported
        ProcessCountMetric()
    ]

    device_count = int(nvmlDeviceGetCount())
    driver_version = nvmlSystemGetDriverVersion()

    device_count_metric = Gauge('nvidia_device_count', 'Number of compute devices in the system', [DRIVER_VERSION_LABEL])
    device_count_metric.labels(driver_version).set_function(lambda: int(nvmlDeviceGetCount())) # Could change if a GPU dies

    for device_index in range(device_count):
        handle = nvmlDeviceGetHandleByIndex(device_index)
        name = nvmlDeviceGetName(handle)

        for metric in metrics:
            metric.prometheus_metric.labels(device_index, name, driver_version).set_function(metric.collect_fn(handle))
