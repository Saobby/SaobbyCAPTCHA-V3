import redis_api
from config import CHALLENGE_EXPIRATION_TIME, TOKEN_EXPIRATION_TIME, REDIS_PREFIX, RATE_LIMIT_TIME_INTERVAL, RATE_LIMIT_MAX_AMOUNT, RATE_LIMIT_BAN_DURATION, RATE_LIMIT_ENABLE_PENALTY, BYPASS_EXPIRATION_TIME, BYPASS_TIMES
import pickle
from util import gen_random_str


def exceeded_rate_limit(user_id: str) -> bool:
    """
    检查用户是否达到速率限制。每调用一次都会给当前用户计一次数
    :param user_id: 用户 id
    :return: 是一个 bool, 如果达到限制则为 True, 否则为 False
    """
    key = REDIS_PREFIX+"rate_limit_"+user_id
    with redis_api.RedisSession() as db_session:
        user_data = db_session.get(key)
        if user_data is None:  # 没有记录
            db_session.setex(key, RATE_LIMIT_TIME_INTERVAL, pickle.dumps({"count": 1}))
            return False
        user_data = pickle.loads(user_data)
        if user_data["count"] >= RATE_LIMIT_MAX_AMOUNT:
            db_session.setex(REDIS_PREFIX+"ban_"+user_id, RATE_LIMIT_BAN_DURATION, "True")  # 惩罚机制:如果触发速率限制, 会被禁止跳过验证码一段时间
            return True
        user_data["count"] += 1
        db_session.set(key, pickle.dumps(user_data), keepttl=True)
        return False


def can_bypass(user_id: str) -> bool:
    """
    判断用户是否可以跳过验证，如果可以会给可用次数减一
    :param user_id: 用户 id
    :return: 是一个 bool，如果可以跳过则为 True，否则为 False
    """
    key = REDIS_PREFIX+"bypass_"+user_id
    with redis_api.RedisSession() as db_session:
        if RATE_LIMIT_ENABLE_PENALTY and db_session.get(REDIS_PREFIX+"ban_"+user_id) is not None:
            return False  # 惩罚机制:如果触发速率限制, 会被禁止跳过验证码一段时间
        user_data = db_session.get(key)
        if user_data is None:  # 没有记录
            return False
        user_data = pickle.loads(user_data)
        if user_data["remaining"] > 0:
            user_data["remaining"] -= 1
            db_session.set(key, pickle.dumps(user_data), keepttl=True)
            return True
        return False


def reset_bypass(user_id: str) -> None:
    """
    重置用户的跳过验证码次数和有效时间
    :param user_id:
    :return: None
    """
    with redis_api.RedisSession() as db_session:
        db_session.setex(REDIS_PREFIX+"bypass_"+user_id, BYPASS_EXPIRATION_TIME, pickle.dumps({"remaining": BYPASS_TIMES}))


def gen_token() -> str:
    """
    生成一个新的 token
    :return: 一个 str, 为生成的 token
    """
    token = gen_random_str(8)
    with redis_api.RedisSession() as db_session:
        db_session.setex(REDIS_PREFIX+"token_"+token, TOKEN_EXPIRATION_TIME, "True")
    return token


def verify_token(token: str) -> bool:
    """
    校验 token 是否有效, 同时在有效时删除该 token
    :param token: 要校验的 token
    :return: 一个 bool，有效时为 True, 否则为 False
    """
    key = REDIS_PREFIX+"token_"+token
    with redis_api.RedisSession() as db_session:
        if db_session.get(key) is None:
            return False
        db_session.delete(key)
        return True


def bind_challenge_id_with_user(challenge_id: str, user_id: str) -> None:
    """
    将一个验证码 id 与一个用户绑定起来
    :param challenge_id: 验证码 id
    :param user_id: 用户 id
    :return: None
    """
    with redis_api.RedisSession() as db_session:
        db_session.setex(REDIS_PREFIX+"challenge_info_"+challenge_id, CHALLENGE_EXPIRATION_TIME, pickle.dumps({"user_id": user_id}))


def get_challenge_id_user(challenge_id: str):
    """
    获取一个验证码 id 绑定的用户
    :param challenge_id: 验证码 id
    :return: 是一个 str, 为用户 id，验证码 id 不存在时会返回 None
    """
    with redis_api.RedisSession() as db_session:
        info = db_session.get(REDIS_PREFIX+"challenge_info_"+challenge_id)
        if info is None:
            return None
        info = pickle.loads(info)
        return info["user_id"]
