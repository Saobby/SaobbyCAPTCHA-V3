import threading
import image_generator
import pickle
import redis_api
from config import IMAGE_POOL_SIZE, REDIS_PREFIX, CHALLENGE_EXPIRATION_TIME, CHALLENGE_FONT_SIZE, DO_INIT
from util import gen_random_str
import base64

generator_lock = threading.Lock()  # 创建锁，保证同时最多有1个线程在生成图片


def fill_pool():
    if not generator_lock.acquire(False):
        return  # 已有线程在运行，直接退出
    try:
        key = REDIS_PREFIX+"image_pool"
        with redis_api.RedisSession() as db_session:
            while True:
                required = IMAGE_POOL_SIZE - db_session.llen(key)
                if required <= 0:
                    break  # 池已填满
                for _ in range(required):
                    db_session.lpush(key, pickle.dumps(image_generator.gen_challenge()))
    finally:
        generator_lock.release()  # 结束之后释放锁


def get_challenge():
    if IMAGE_POOL_SIZE <= 0:
        return image_generator.gen_challenge()
    with redis_api.RedisSession() as db_session:
        challenge = db_session.rpop(REDIS_PREFIX+"image_pool", )
        thread = threading.Thread(target=fill_pool)
        thread.start()  # 回填池
        if challenge is None:
            return image_generator.gen_challenge()  # 如果池是空的就实时生成
        return pickle.loads(challenge)  # 否则先使用池中的


def base64_encode(sth: bytes):
    """
    将一段 bytes 进行 base64 编码
    :param sth: 要编码的 bytes
    :return: 结果，是一个 str
    """
    return base64.b64encode(sth).decode()


def calculate_distance(x0: [int, float], y0: [int, float], x1: [int, float], y1: [int, float]) -> float:
    """
    计算两个点(x0, y0)和(x1, y1)之间的距离
    :param x0:
    :param y0:
    :param x1:
    :param y1:
    :return: 距离
    """
    return ((x0-x1)**2+(y0-y1)**2)**0.5


def create_captcha() -> tuple[str, str, str]:
    """
    创建一个验证码
    :return: 是一个 tuple.
        第一项是一个 str, 为验证码 id
        第二项是一个 str, 为提示图片的 url
        第三项是一个 str, 为验证图片的 url
    """
    challenge = get_challenge()
    challenge_id = gen_random_str(8)
    with redis_api.RedisSession() as db_session:
        db_session.setex(REDIS_PREFIX+"challenge_"+challenge_id, CHALLENGE_EXPIRATION_TIME, pickle.dumps(challenge))
    return challenge_id, \
        "data:image/jpg;base64,"+base64_encode(challenge[2]), \
        "data:image/jpg;base64,"+base64_encode(challenge[3])


def verify_answer(challenge_id: str, pos_list: list[tuple[int, int]]) -> bool:
    """
    验证用户的答案是否正确
    :param challenge_id: 验证码 id
    :param pos_list: 用户点击的坐标列表，格式为[(x0, y0), (x1, y1), ...]
    :return: 是一个 bool, 如果答案正确则为 True, 否则为 False
    """
    key = REDIS_PREFIX+"challenge_"+challenge_id
    with redis_api.RedisSession() as db_session:
        challenge = db_session.get(key)
        if challenge is None:  # 挑战不存在或已过期
            return False
        challenge = pickle.loads(challenge)
        users_word = ""  # 用户点选的词汇
        check_pos_list = challenge[1]
        for users_x, users_y in pos_list:
            users_chr = None
            for check_chr, check_x, check_y in check_pos_list:
                if calculate_distance(users_x, users_y, check_x, check_y) <= CHALLENGE_FONT_SIZE / 2 * 1.2:
                    users_chr = check_chr
                    check_pos_list.remove((check_chr, check_x, check_y))
                    break
            if users_chr is None:  # 用户没有点到任何字上
                db_session.delete(key)  # 用户没有答对，这个挑战作废
                return False
            users_word += users_chr
        if users_word != challenge[0]:  # 用户拼出的词语和答案不同
            db_session.delete(key)
            return False
        db_session.delete(key)  # 用户答对了，这个挑战作废。防止重放攻击
        return True  # 答对了


if DO_INIT:
    threading.Thread(target=fill_pool).start()
