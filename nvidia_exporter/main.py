import atexit
import time

import pynvml
from prometheus_client import make_wsgi_app
from wsgiref.simple_server import make_server

from .stats import NvidiaStats
from .prometheus_metrics import build_metrics

if __name__ == '__main__':
    try:
        pynvml.nvmlInit()
        atexit.register(pynvml.nvmlShutdown)

        build_metrics()
        app = make_wsgi_app()
        httpd = make_server('', 9200, app)
        httpd.serve_forever()
    except pynvml.NVMLError, err:
        print("NVML error: %s" % err)
