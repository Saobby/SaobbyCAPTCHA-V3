import gevent.monkey
gevent.monkey.patch_all()
import multiprocessing
from config import REAL_IP_HEADER, GUNICORN_PORT, GUNICORN_LOG_LEVEL

loglevel = GUNICORN_LOG_LEVEL
bind = f"0.0.0.0:{GUNICORN_PORT}"
pidfile = "./gunicorn.pid"
logfile = "-"
errorlog = "-"
accesslog = "-"
access_log_format = '%({real_ip_header}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'.replace("real_ip_header", REAL_IP_HEADER)
capture_output = True

workers = multiprocessing.cpu_count()
worker_class = "gunicorn.workers.ggevent.GeventWorker"
