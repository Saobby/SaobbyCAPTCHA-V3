from config import LOGS_DIR, BACKGROUND_IMAGES_DIR, FONTS_DIR, WORDS_PATH
import os

# 创建必要的目录和文件
if not os.path.isdir(LOGS_DIR):
    os.makedirs(LOGS_DIR)
if not os.path.isdir(BACKGROUND_IMAGES_DIR):
    os.makedirs(BACKGROUND_IMAGES_DIR)
if not os.path.isdir(FONTS_DIR):
    os.makedirs(FONTS_DIR)
if not os.path.isfile(WORDS_PATH):
    with open(WORDS_PATH, "w", encoding="utf-8") as f:
        f.write("")

program_conf = f"""
[program:saobby_captcha_v3]
command=gunicorn -c gunicorn.py wsgi:app --chdir /app
directory=/app
startsecs=3
stopwaitsecs=3
stdout_logfile={LOGS_DIR}/access.log
stdout_logfile_backups=4
stderr_logfile={LOGS_DIR}/error.log
stderr_logfile_backups=4
"""
with open("./program.conf", "w", encoding="utf-8") as f:
    f.write(program_conf)

if os.path.isfile("./gunicorn.pid"):
    os.remove("./gunicorn.pid")

os.system("supervisord -n -c ./supervisord.conf")
