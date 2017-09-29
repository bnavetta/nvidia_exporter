import functools
from prometheus_client import Gauge
from pynvml import *


class Metric(object):
    __slots__ = ['_collect', '_base_metric']

    def __init__(self, name, description, collect_fn):
        self._collect = collect_fn
        self._base_metric = Gauge('nvidia_' + name, description, ['device_index', 'device_name'])

    def metric_for(self, device_name, device_index, device_handle):
        m = self._base_metric.labels(device_index=device_index, device_name=device_name)
        m.set_function(functools.partial(self._collect, device_handle))
        return m

# Metrics from v1 that don't seem super useful
# class GPUUtilizationMetric(Metric):
#     def __init__(self):
#         super(GPUUtilizationMetric, self).__init__(
#             'gpu_util',
#             'Percent of time over the past sample period during which one or more kernels was executing on the GPU'
#         )
#
#     def collect(self, handle):
#         return nvmlDeviceGetUtilizationRates(handle).gpu
#
# class MemoryUtilizationMetric(Metric):
#     def __init__(self):
#         super(MemoryUtilizationMetric, self).__init__(
#             'mem_util',
#             'Percent of time over the past sample period during which global (device) memory was being read or written'
#         )
#
#     def collect(self, handle):
#         return nvmlDeviceGetUtilizationRates(handle).memory
#
# class FanSpeedMetric(Metric):
#     def __init__(self):
#         super(FanSpeedMetric, self).__init__(
#             'fan_speed',
#             'Fan speed as a percent of the maximum, assuming the fan is not physically blocked'
#         )
#
#     def collect(self, handle):
#         try:
#             return nvmlDeviceGetFanSpeed(handle)
#         except NVMLError, nvmlError:
#             # Some GPUs don't have fans
#             if nvmlError.value == NVML_ERROR_NOT_SUPPORTED:
#                 return 0
#
# class PowerUsageMetric(Metric):
#     def __init__(self):
#         super(PowerUsageMetric, self).__init__(
#             'power_usage_W',
#             'Power usage in watts for the GPU and associated circuitry (e.g. memory)'
#         )
#
#     def collect(self, handle):
#         return nvmlDeviceGetPowerUsage(handle) / 1000
#
# class PowerManagementLimitMetric(Metric):
#     def __init__(self):
#         super(PowerManagementLimitMetric, self).__init__(
#             'power_management_limit_W',
#             'Upper limit for power draw at which the power management algorithm kicks in (in watts)'
#         )
#
#     def collect(self, handle):
#         return nvmlDeviceGetPowerManagementLimit(handle) / 1000
#
# class ECCDoubleBitErrorsMetric(Metric):
#     def __init__(self):
#         super(ECCDoubleBitErrorsMetric, self).__init__(
#             'ecc_db_errors',
#             'Count of double-bit (uncorrected) ECC errors over the lifetime of the device'
#         )
#
#     def collect(self, handle):
#         return nvmlDeviceGetTotalEccErrors(handle, 1, 1)
#
# class ECCSingleBitErrorsMetric(Metric):
#     def __init__(self):
#         super(ECCSingleBitErrorsMetric, self).__init__(
#             'ecc_sb_errors',
#             'Count of single-bit (corrected) ECC errors over the lifetime of the device'
#         )
#
#     def collect(self, handle):
#         return nvmlDeviceGetTotalEccErrors(handle, 0, 1)
