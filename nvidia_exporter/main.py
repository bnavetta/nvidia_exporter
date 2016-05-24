import atexit
import time

try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    # Python 3
    from http.server import BaseHTTPRequestHandler, HTTPServer

import pynvml
from prometheus_client import MetricsHandler

from .stats import NvidiaStats
from .prometheus_metrics import build_metrics

def main():
    try:
        pynvml.nvmlInit()
        atexit.register(pynvml.nvmlShutdown)

        build_metrics()
        httpd = HTTPServer(('', 9200), MetricsHandler)
        httpd.serve_forever()

    except pynvml.NVMLError, err:
        print("NVML error: %s" % err)

if __name__ == '__main__':
    main()
