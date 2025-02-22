import sys
import requests
import json
from config import GUNICORN_PORT

try:
    rsp = requests.post(f"http://127.0.0.1:{GUNICORN_PORT}/api/gen_challenge", timeout=3)
    rsp = json.loads(rsp.text)
    if rsp["retcode"]:
        sys.exit(1)  # unhealthy
    sys.exit(0)
except:
    sys.exit(1)  # unhealthy
