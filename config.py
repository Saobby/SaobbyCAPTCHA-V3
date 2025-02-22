import os

# 存放背景图片的目录，每次生成验证码图片会随机从其中选择一个
BACKGROUND_IMAGES_DIR = "./backgrounds"
# 存放字体的目录，每次生成验证码图片会随机从其中选择一个
FONTS_DIR = "./fonts"
# 存放词汇列表(一行一个)的文本文件(UTF-8编码)，每次生成验证码图片会随机从其中选择一个
WORDS_PATH = "./words.txt"

# 提示文本图片的字体大小
TIP_FONT_SIZE = 30 if os.environ.get("TIP_FONT_SIZE") is None else int(os.environ.get("TIP_FONT_SIZE"))
# 验证码图片中文字的大小
CHALLENGE_FONT_SIZE = 45 if os.environ.get("CHALLENGE_FONT_SIZE") is None else int(os.environ.get("CHALLENGE_FONT_SIZE"))
# 提示文本图片的字体最大旋转角度
TIP_MAX_ROTATE_ANGLE = 20 if os.environ.get("TIP_MAX_ROTATE_ANGLE") is None else int(os.environ.get("TIP_MAX_ROTATE_ANGLE"))
# 验证码图片的字体最大旋转角度
CHALLENGE_MAX_ROTATE_ANGLE = 45 if os.environ.get("CHALLENGE_MAX_ROTATE_ANGLE") is None else int(os.environ.get("CHALLENGE_MAX_ROTATE_ANGLE"))

# 在空闲时，程序会预先生成一些验证码图片，以便在访问量突然变大时快速应对
# 当预先生成的图片被消耗后，程序会自动填补新的图片，使可用的图片维持在一定数量
# 设置维持的数量的大小(设为 0 来禁用预生成)
IMAGE_POOL_SIZE = 500 if os.environ.get("IMAGE_POOL_SIZE") is None else int(os.environ.get("IMAGE_POOL_SIZE"))

# 验证码的完成时限(单位: s)
CHALLENGE_EXPIRATION_TIME = 300 if os.environ.get("CHALLENGE_EXPIRATION_TIME") is None else int(os.environ.get("CHALLENGE_EXPIRATION_TIME"))
# 验证码完成后获得的 token 的有效期(单位: s)
TOKEN_EXPIRATION_TIME = 120 if os.environ.get("TOKEN_EXPIRATION_TIME") is None else int(os.environ.get("TOKEN_EXPIRATION_TIME"))

# 速率限制的测速区间(单位: s)
RATE_LIMIT_TIME_INTERVAL = 10 if os.environ.get("RATE_LIMIT_TIME_INTERVAL") is None else int(os.environ.get("RATE_LIMIT_TIME_INTERVAL"))
# 在 1 个测速区间内，最多访问的次数
RATE_LIMIT_MAX_AMOUNT = 10 if os.environ.get("RATE_LIMIT_MAX_AMOUNT") is None else int(os.environ.get("RATE_LIMIT_MAX_AMOUNT"))
# 达到速率限制时，是否认为该用户为可疑用户，并对其进行惩罚
# 惩罚: 成功完成一个验证码后，后几次仍然需要完成
RATE_LIMIT_ENABLE_PENALTY = True if os.environ.get("RATE_LIMIT_ENABLE_PENALTY") is None else os.environ.get("RATE_LIMIT_ENABLE_PENALTY").lower() == "true"
# 惩罚有效时间(单位: s)
RATE_LIMIT_BAN_DURATION = 3600 * 4 if os.environ.get("RATE_LIMIT_BAN_DURATION") is None else int(os.environ.get("RATE_LIMIT_BAN_DURATION"))

# 完成一个验证码后，后面的多少次可以不用再完成
BYPASS_TIMES = 5 if os.environ.get("BYPASS_TIMES") is None else int(os.environ.get("BYPASS_TIMES"))
# 完成一个验证码后，后面几次可不用再完成的效果的有效期(单位: s)
BYPASS_EXPIRATION_TIME = 300 if os.environ.get("BYPASS_EXPIRATION_TIME") is None else int(os.environ.get("BYPASS_EXPIRATION_TIME"))

# Redis 地址
REDIS_HOST = "redis" if os.environ.get("REDIS_HOST") is None else os.environ.get("REDIS_HOST")
# Redis 端口
REDIS_PORT = 6399 if os.environ.get("REDIS_PORT") is None else int(os.environ.get("REDIS_PORT"))
# Redis 用户名(如果没有设置请留空)
REDIS_USERNAME = "" if os.environ.get("REDIS_USERNAME") is None else os.environ.get("REDIS_USERNAME")
# Redis 访问密码(如果没有设置请留空)
REDIS_PASSWORD = "" if os.environ.get("REDIS_PASSWORD") is None else os.environ.get("REDIS_PASSWORD")
# Redis 请求超时时，是否重试
REDIS_RETRY_ON_TIMEOUT = True if os.environ.get("REDIS_RETRY_ON_TIMEOUT") is None else os.environ.get("REDIS_RETRY_ON_TIMEOUT").lower() == "true"
# 连接池的最大连接数
REDIS_MAX_CONNECTIONS = 1024 if os.environ.get("REDIS_MAX_CONNECTIONS") is None else int(os.environ.get("REDIS_MAX_CONNECTIONS"))

# 程序向 Redis 中存储内容时键的前缀(如果多个本验证码系统依赖同一个 Redis 实例，请设置不同的前缀)
REDIS_PREFIX = "saobby_captcha_" if os.environ.get("REDIS_PREFIX") is None else os.environ.get("REDIS_PREFIX")

# 用于获取用户真实 IP 的请求头(比如 x-forwarded-for)，留空则使用网络连接中的 IP
REAL_IP_HEADER = "" if os.environ.get("REAL_IP_HEADER") is None else os.environ.get("REAL_IP_HEADER")

# 程序启动时，是否进行初始化操作
# 初始化操作包括:
#   将所有背景图片缩放到所需要的尺寸，并转换为 jpg 格式
#   开始填充图片池
DO_INIT = True if os.environ.get("DO_INIT") is None else os.environ.get("DO_INIT").lower() == "true"

# 设置响应头中 Access-Control-Allow-Origin 的值
# 如果设置为 * , 则会赋值为请求头中 Origin 的值(老旧浏览器不支持通配符)
CORS_ORIGIN = "*" if os.environ.get("CORS_ORIGIN") is None else os.environ.get("CORS_ORIGIN")

# 设置你的网站后端用于校验 token 的 API 的访问路径
# 由于本接口没有速率限制，应尽量避免外部访问，因此请设置一个其他人猜不到的路径
API_VERIFY_TOKEN_PATH = "/api/verify_token"

# 设置是否启用测试页面，启用后，在访问根路径时会显示一个测试页面
ENABLE_TEST_PAGE = True if os.environ.get("ENABLE_TEST_PAGE") is None else os.environ.get("ENABLE_TEST_PAGE").lower() == "true"

# Gunicorn 监听的端口
GUNICORN_PORT = 5000 if os.environ.get("GUNICORN_PORT") is None else int(os.environ.get("GUNICORN_PORT"))
# Gunicorn 日志级别
GUNICORN_LOG_LEVEL = "warning" if os.environ.get("GUNICORN_LOG_LEVEL") is None else os.environ.get("GUNICORN_LOG_LEVEL")

# 访问日志和错误日志的存放目录
LOGS_DIR = "./log" if os.environ.get("LOGS_DIR") is None else os.environ.get("LOGS_DIR")
