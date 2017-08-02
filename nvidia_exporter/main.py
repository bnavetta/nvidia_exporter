import atexit
import sys

try:
    from BaseHTTPServer import HTTPServer
except ImportError:
     from http.server import HTTPServer

import pynvml
from prometheus_client import MetricsHandler

from .metrics_builder import build_metrics

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9200

    try:
        pynvml.nvmlInit()
        atexit.register(pynvml.nvmlShutdown)

        build_metrics()

        print('Starting on port {}'.format(port))
        httpd = HTTPServer(('', port), MetricsHandler)
        httpd.serve_forever()

    except pynvml.NVMLError, err:
        print('NVML error: {}'.format(err))

if __name__ == '__main__':
    main()
