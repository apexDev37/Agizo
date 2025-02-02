"""Gunicorn config.

Optimizes Gunicorn for handling Django requests efficiently.
Leverages multiple workers and threads for concurrency, sets timeouts for
graceful shutdowns, and logs output to stdout.
"""

import multiprocessing

bind = "0.0.0.0:10000"
workers = multiprocessing.cpu_count() * 2 + 1  # Recommended formula for workers
threads = 2  # Handle blocking I/O with threads
worker_class = "gthread"
timeout = 30
graceful_timeout = 30
loglevel = "info"
accesslog = "-"
errorlog = "-"
keepalive = 5
preload_app = True
