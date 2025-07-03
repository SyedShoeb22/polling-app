import multiprocessing
import os

# Set environment variables
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SCHMGM.settings")

bind = "0.0.0.0:8000"

workers = multiprocessing.cpu_count() * 2 + 1
errorlog = "errorlog/gunicorn_error.log"  # Specify the path to your error log file relative to the root folder
loglevel = "info"

# Optional: Daemonize Gunicorn
daemon = True
pidfile = "gunicorn.pid"  # Specify the path to the PID file relative to the root folder
