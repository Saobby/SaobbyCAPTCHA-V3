from flask import Flask, request, render_template, abort
from server_util import gen_return, rate_limit, check_args, get_client_ip
from config import CORS_ORIGIN, API_VERIFY_TOKEN_PATH, ENABLE_TEST_PAGE
import user_service
import captcha_service

app = Flask(__name__)


@app.route("/")
def index():
    if ENABLE_TEST_PAGE:
        return render_template("test.html")
    return abort(404)


@app.route("/api/gen_challenge", methods=["post"])
@rate_limit
def api_gen_challenge():
    ip = get_client_ip()
    if user_service.can_bypass(ip):  # 检查用户是否可以跳过验证码
        token = user_service.gen_token()
        return gen_return(0, "OK", {"token": token})
    challenge_id, tip_img_url, challenge_img_url = captcha_service.create_captcha()
    user_service.bind_challenge_id_with_user(challenge_id, ip)
    return gen_return(0, "OK", {"id": challenge_id, "tip": tip_img_url, "challenge": challenge_img_url})


@app.route("/api/get_token", methods=["post"])
@check_args("id_", "pos")
@rate_limit
def api_get_token(id_: str, pos: list):
    user = user_service.get_challenge_id_user(id_)
    ip = get_client_ip()
    if user != ip:  # 创建验证码的 IP 与提交验证的 IP 不一致
        return gen_return(1, "验证失败,请重试")
    result = captcha_service.verify_answer(id_, pos)
    if not result:
        return gen_return(1, "验证失败,请重试")
    user_service.reset_bypass(ip)  # 让用户之后几次可以跳过验证
    token = user_service.gen_token()
    return gen_return(0, "OK", {"token": token})


@app.route(API_VERIFY_TOKEN_PATH, methods=["post"])
@check_args("token")
def api_verify_token(token: str):
    return gen_return(0, "OK", {"result": user_service.verify_token(token)})


@app.errorhandler(400)
def error_400(err):
    return gen_return(400, "参数错误"), 400


@app.errorhandler(404)
def error_404(err):
    return gen_return(404, "你要访问的 API 不存在"), 404


@app.errorhandler(500)
def error_500(err):
    return gen_return(500, "服务器内部错误, 请稍后再试"), 500


@app.after_request
def add_header(rsp):
    if CORS_ORIGIN == "*":
        if request.headers.get("origin") is not None:
            rsp.headers["Access-Control-Allow-Origin"] = request.headers.get("origin")
        else:
            rsp.headers["Access-Control-Allow-Origin"] = "*"
    else:
        rsp.headers["Access-Control-Allow-Origin"] = CORS_ORIGIN
    rsp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    rsp.headers["Access-Control-Allow-Credentials"] = "true"
    rsp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    rsp.headers["Access-Control-Max-Age"] = "600"
    return rsp


if __name__ == "__main__":
    app.run(port=9876)
