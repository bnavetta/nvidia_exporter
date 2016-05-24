from .stats import NvidiaStats

from prometheus_client import Gauge

def build_metrics():
    stats = NvidiaStats()

    device_count = Gauge('nvidia_device_count', 'Number of available devices')
    device_count.set_function(stats.device_count)

    for device_index in range(0, stats.device_count()):
        label_names = ['device_index', 'device_name']
        label_values = {'device_index': device_index, 'device_name': stats.device_name(device_index)}

        gpu_temp = Gauge('nvidia_gpu_temp', 'GPU Temperature (degrees Celsius)', label_names)
        gpu_temp.labels(label_values).set_function(lambda: stats.gpu_temp(device_index))

        fan_speed = Gauge('nvidia_fan_speed', 'Fan speed (percentage)', label_names)
        fan_speed.labels(label_values).set_function(lambda: stats.device_fan_speed(device_index))

        power_usage = Gauge('nvidia_power_usage', 'Power usage (milliwats)', label_names)
        power_usage.labels(label_values).set_function(lambda: stats.device_power_usage(device_index))

        power_limit = Gauge('nvidia_power_limit', 'Power limit (milliwats)', label_names)
        power_limit.labels(label_values).set_function(lambda: stats.device_power_limit(device_index))

        free_memory = Gauge('nvidia_memory_free', 'Free memory (bytes)', label_names)
        free_memory.labels(label_values).set_function(lambda: stats.device_free_memory(device_index))

        used_memory = Gauge('nvidia_memory_used', 'Used memory (bytes)', label_names)
        used_memory.labels(label_values).set_function(lambda: stats.device_used_memory(device_index))

        total_memory = Gauge('nvidia_memory_total', 'Total memory (bytes)', label_names)
        total_memory.labels(label_values).set_function(lambda: stats.device_total_memory(device_index))

        graphics_processes = Gauge('nvidia_graphics_processes', 'Count of graphics processes', label_names)
        graphics_processes.labels(label_values).set_function(lambda: stats.graphics_processes(device_index))

        compute_processes = Gauge('nvidia_compute_processes', 'Count of compute processes', label_names)
        compute_processes.labels(label_values).set_function(lambda: stats.compute_processes(device_index))
