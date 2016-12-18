import atexit
import sys

import pynvml
from prometheus_client import MetricsHandler

from .metrics_builder import build_metrics

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9200

    try:
        pynvml.nvmlInit()
        atexit.register(pynvml.nvmlShutdown)

        build_metrics()

        httpd = HTTPServer(('', port), MetricsHandler)
        httpd.serve_forever()

    except pynvml.NVMLError, err:
        print("NVML error: %s" % err)

if __name__ == '__main__':
    main()
