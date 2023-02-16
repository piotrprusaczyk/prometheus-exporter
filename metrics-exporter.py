import psutil
from prometheus_client import start_http_server, Metric, REGISTRY
import time

class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        # Get the CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        metric_cpu = Metric('cpu_usage', 'CPU Usage', 'gauge')
        metric_cpu.add_sample('cpu_usage', value=cpu_usage, labels={})
        yield metric_cpu

        # Get the RAM usage
        mem_usage = psutil.virtual_memory().percent
        metric_mem = Metric('mem_usage', 'Memory Usage', 'gauge')
        metric_mem.add_sample('mem_usage', value=mem_usage, labels={})
        yield metric_mem

        # Get the disk usage
        disk_usage = psutil.disk_usage('/')
        metric_disk = Metric('disk_usage', 'Disk Usage', 'gauge')
        metric_disk.add_sample('disk_usage_total', value=disk_usage.total/1024/1024/1024, labels={})
        metric_disk.add_sample('disk_usage_used', value=disk_usage.used/1024/1024/1024, labels={})
        metric_disk.add_sample('disk_usage_free', value=disk_usage.free/1024/1024/1024, labels={})
        yield metric_disk
     

if __name__ == '__main__':
    # Start the server to expose the metrics
    start_http_server(8000)

    # Register the custom collector
    REGISTRY.register(CustomCollector())

    # Run the server forever
    while True:
        time.sleep(60)

