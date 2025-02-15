from flask import jsonify, Response, request, abort
from config import REAL_IP_HEADER
import user_service
from functools import wraps


def gen_return(retcode: int, msg: str, data=None) -> Response:
    """
    生成一个 JSON 响应
    :param retcode: 错误码
    :param msg: 消息
    :param data: 数据
    :return: 返回一个 flask 的响应对象
    """
    return jsonify({"retcode": retcode, "msg": msg, "data": data})


def get_client_ip() -> str:
    """
    获取客户端的 IP 地址
    :return: 一个 str, 是客户端的 IP 地址
    """
    if REAL_IP_HEADER:
        return request.headers.get(REAL_IP_HEADER)
    return request.remote_addr


def rate_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ip = get_client_ip()
        if user_service.exceeded_rate_limit(ip):
            return gen_return(429, "请求过于频繁"), 429
        return func(*args, **kwargs)
    return wrapper


def check_args(*required_args):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.json is None:
                return abort(400)
            args_dict = {}
            for arg in required_args:
                val = request.json.get(arg)
                if val is None:
                    return abort(400)
                args_dict[arg] = val
            return func(*args, **kwargs, **args_dict)
        return wrapper
    return decorator
