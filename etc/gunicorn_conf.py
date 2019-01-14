# For configuration details go to:
# http://docs.gunicorn.org/en/19.7.1/configure.html
import multiprocessing

# Server Socket
backlog = 2048  # default
bind = "0.0.0.0:5000"

# Worker Processes
graceful_timeout = 90
keepalive = 2  # default
max_requests = 0  # default
timeout = 2000
worker_class = "sync"
worker_connections = 1000  # default
workers = multiprocessing.cpu_count() * 2 + 1
# workers = 1

# Security
limit_request_fields = 100  # default
limit_request_field_size = 8190  # default
limit_request_line = 4094  # default

# Debugging
debug = True
reload = True

# Server Mechanics
chdir = "/code"
daemon = False  # default
group = 0  # default
pidfile = "/var/run/gunicorn.pid"
umask = 0  # default
user = 0  # default

# Logging
accesslog = "-"
errorlog = "-"  # default
loglevel = "info"
