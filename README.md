# SaobbyCAPTCHA-V3
 一个基于汉字点选的简单易用、可配置的人机验证系统。
- - - - -
# 预览


https://github.com/user-attachments/assets/682f324c-f08e-4ade-834f-b3d34c1d2b94


[在线预览](https://captcha-v3.saobby.com/)
# 功能
- 在完成一次验证码后，后几次可以不用再完成
- 在空闲时预生成验证码图片，以应对突然的高并发访问
- 启用速率限制，阻止过快的访问，并要求高危用户总是需要完成验证码
- 设置每个验证码最大完成时限
- 自定义背景图片和字体等
# 安装和使用
## 准备好背景图片、字体和词语
1. 创建项目目录，创建背景图片、字体目录  
  ```bash
  mkdir captcha
  mkdir captcha/backgrounds
  mkdir captcha/fonts
  ```
2. 放置背景图和字体  
  准备一些 jpg 或 png 格式的图片，尺寸不要太大，把他们放入刚刚创建的`captcha/backgrounds`目录。当生成验证码图片的时候，会随机从其中选一个作为背景图。
  再准备几个 ttf 格式的字体，把他们放入刚刚创建的`captcha/fonts`目录。当生成每个字的图案时，会随机选择一个字体。
3. 设置词语  
  创建一个文件，用来放置验证码的词语。  
  ```bash
  touch captcha/words.txt
  ```
  在里面填入你想要在验证码中出现的词语，**每个词语字数 2~5 个字**(字数不在范围内的词语会被忽略)，**一行一个**，每次生成验证码会从中随机选取一个。  
4. 创建日志目录  
  创建一个目录用来存放访问日志和错误日志  
  ```bash
  mkdir captcha/log
  ```
## 使用 Docker 部署
确保你的服务器上已经安装了 [Docker](https://www.docker.com/) 和 [Redis](https://redis.io/) (**版本>=6.0**)。  
1. 启动容器  
  下面是一条启动指令的示例，请根据你的实际情况修改:  
  ```bash
  docker run -d\
  -p {port}:5000\
  -v captcha/backgrounds:/app/backgrounds\
  -v captcha/fonts:/app/fonts\
  -v captcha/log:/app/log\
  -v captcha/words.txt:/app/words.txt\
  -e REDIS_HOST={redis_host}\
  -e REDIS_PORT={redis_port}\
  --restart=unless-stopped\
  axolotltech/saobby-captcha-v3:latest
  ```
  其中，`{port}`是映射到宿主机上的端口，也就是外部访问的端口；`{redis_host}`是 Redis 地址，可以是 IP 或域名，比如 `127.0.0.1`；`{redis_port}`是 Redis 端口；`captcha/backgrounds` 等都是我们刚刚创建的目录。  
  除此之外，其它可配置的环境变量如下:  
  |键|描述|默认值|
  |---|---|---|
  |REDIS_HOST|Redis 服务地址，可以是 IP 或域名|127.0.0.1|
  |REDIS_PORT|Redis 端口|6379|
  |REDIS_USERNAME|Redis 用户名(如果没有设置请留空)| |
  |REDIS_PASSWORD|Redis 访问密码(如果没有设置请留空)| |
  |REDIS_RETRY_ON_TIMEOUT|Redis 请求超时时，是否重试|true|
  |REDIS_MAX_CONNECTIONS|Redis 连接池的最大连接数|1024|
  |REDIS_PREFIX|程序向 Redis 中存储内容时键的前缀(如果多个本验证码系统依赖同一个 Redis 实例，请设置不同的前缀)|saobby_captcha_|
  |REAL_IP_HEADER|用于获取用户真实 IP 的请求头(比如 x-forwarded-for)，留空则使用网络连接中的 IP| |
  |CORS_ORIGIN|设置响应头中 Access-Control-Allow-Origin 的值。如果设置为 * , 则会赋值为请求头中 Origin 的值(老旧浏览器不支持通配符)|*|
  |API_VERIFY_TOKEN_PATH|设置你的网站后端用于校验 token 的 API 的访问路径。由于本接口没有速率限制，应尽量避免外部访问，因此请设置一个其他人猜不到的路径。|/api/verify_token|
  |ENABLE_TEST_PAGE|设置是否启用测试页面，启用后，在访问根路径时会显示一个测试页面|true|
  |IMAGE_POOL_SIZE|在空闲时，程序会预先生成一些验证码图片，以便在访问量突然变大时快速应对。当预先生成的图片被消耗后，程序会自动填补新的图片，使可用的图片维持在一定数量。设置维持的数量的大小(设为 0 来禁用预生成)|500|
  |CHALLENGE_EXPIRATION_TIME|验证码的完成时限(单位: s)|300|
  |TOKEN_EXPIRATION_TIME|验证码完成后获得的 token 的有效期(单位: s)(不建议设置太长)|120|
  |RATE_LIMIT_TIME_INTERVAL|速率限制的测速区间(单位: s)|10|
  |RATE_LIMIT_MAX_AMOUNT|在 1 个测速区间内，最多访问的次数|10|
  |RATE_LIMIT_ENABLE_PENALTY|达到速率限制时，是否认为该用户为可疑用户，并对其进行惩罚。惩罚: 成功完成一个验证码后，后几次仍然需要完成。|true|
  |RATE_LIMIT_BAN_DURATION|惩罚有效时间(单位: s)|14400 (4 小时)|
  |BYPASS_TIMES|完成一个验证码后，后面的多少次可以不用再完成|5|
  |BYPASS_EXPIRATION_TIME|完成一个验证码后，后面几次可不用再完成的效果的有效期(单位: s)(不建议设置太长)|300|
  |TIP_FONT_SIZE|提示文本图片的字体大小|30|
  |CHALLENGE_FONT_SIZE|验证码图片中文字的大小|45|
  |TIP_MAX_ROTATE_ANGLE|提示文本图片的字体最大旋转角度|20|
  |CHALLENGE_MAX_ROTATE_ANGLE|验证码图片的字体最大旋转角度|45|
  |BACKGROUND_IMAGES_DIR|容器内存放背景图片的目录，不建议修改，直接修改绑定宿主机的目录即可。|./backgrounds|
  |FONTS_DIR|存放字体的目录，不建议修改，直接修改绑定宿主机的目录即可。|./fonts|
  |WORDS_PATH|存放词汇列表(一行一个)的文本文件(UTF-8编码)，不建议修改，直接修改绑定宿主机的目录即可。|./words.txt|
  |DO_INIT|程序启动时，是否进行初始化操作。初始化操作包括:将所有背景图片缩放到所需要的尺寸，并转换为 jpg 格式(不会重复转换);开始填充图片池; 不建议修改。|true|
  |GUNICORN_PORT|容器内监听的端口。不建议修改，直接修改容器端口映射即可。|5000|
  |GUNICORN_LOG_LEVEL|Gunicorn 日志级别。不建议修改。|warning|
  |LOGS_DIR|容器内访问日志和错误日志的存放目录，不建议修改，直接修改绑定宿主机的目录即可。|./log|
2. 测试一下  
  使用指令`docker ps`查看容器运行状态，如果为`healthy`则部署成功。如果启用了测试页面，也可以访问`http://你的服务器IP:端口/`来打开测试页面测试服务。 **建议再使用 nginx 反向代理本验证码服务，以便对响应进行压缩和配置 SSL 证书**。
## 在前端页面上部署  
可以在`http://你的服务器IP:端口/static/js/saobbyCaptchaV3.js`下载验证码前端 JS，推荐将这个 JS 部署在自己的 CDN 上，来加快用户下载速度。  
之后，在需要人机验证的页面上加载 JS 脚本。  
```html
<script src="https://your-site.com/static/js/saobbyCaptchaV3.js" async></script>
```
之后，你有两种方法使用人机验证。
### 1. 在表单中插入人机验证
下面是一个简单的登录表单的例子:  
```html
<form method="post" action="/login">
     <input type="text" name="username" placeholder="用户名"><br>
     <input type="password" name="password" placeholder="密码"><br>
     <script src="https://your-site.com/static/js/saobbyCaptchaV3.js"></script>
     <div id="captcha-div"></div><br>
     <script>
         const captcha = new SaobbyCaptchaV3({
             apiBaseUrl: "你的验证码服务的访问地址(后文介绍)",
             showTrigger: true,
             container: document.getElementById("captcha-div")
         });
     </script>
     <input type="submit" value="登录">
 </form>
```
这么做之后，当表单提交时，会自动附带上一个`SCV3_token`参数，包含人机验证 token，以供后端验证。
### 2. 自定义使用
如果你希望更灵活的控制验证码弹出的时机，也可以使用脚本控制。下面是一个例子:  
```javascript
const captcha = new SaobbyCaptchaV3({
    apiBaseUrl: "你的验证码服务的访问地址(后文介绍)",
    showTrigger: false,  // 不显示"点击进行人机验证"的框框(后文介绍)
    once: true  // 在进行一次验证之后，自动销毁人机验证对象
});
const result = await captcha.verify();  // 进行人机验证
if (!result.retcode){
    console.log(result.data.token);  // 验证成功
}
```
### 详细说明
`SaobbyCaptchaV3` 是一个类，包含以下几种方法:  
- constructor(options) (创建对象)  
  `options` 是一个 `object`，有以下几个键:
    |键|数据类型|是否必须|说明|默认值|
    |---|---|---|---|---|
    |apiBaseUrl|string|是|验证码系统的公网访问地址，比如`http://你的服务器IP:端口`(末尾没有`/`)。**强烈建议再使用 nginx 反向代理本验证码服务，以便对响应进行压缩和配置 SSL 证书**|无|
    |showTrigger|bool|否|是否显示"点击进行人机验证"的框框|false|
    |container|DOM 元素|否|设置验证码组件要放在哪个元素内(见示例)。如果设置了`showTrigger`为`true`则此项必须指定。|如果不指定会自动创建一个`div`标签用于放置组件|
    |once|bool|否|在验证完一次后，是否销毁人机验证对象。如果设置了`showTrigger`为`true`则不能设置本项为`true`|false|
- verify()  
  返回一个 `Promise`。调用时会进行人机验证，并返回结果。  
  这个 `Promise` 只会 resolve。  
  返回的结果是一个 `object`，结构如下:  
  |键|数据类型|说明|示例|
  |---|---|---|---|
  |retcode|integer|结果的类型|`0`: 验证成功; `1`: 用户点了×关闭验证窗口; `429`: 请求过于频繁; `500`: 服务器内部错误; `-1`: 网络错误;|
  |msg|string|错误消息|"用户取消了验证"|
  |data|object|数据值|{token: "验证码tokenxxxxxxx"}|
- destroy()  
  手动将验证码的 HTML 从 DOM 中移除。
## 在后端验证前端传来的验证码 token
前端完成验证码后会得到一个验证码 token，并发送给后端。后端需要验证 token 的有效性，如果有效，则证明用户是真人。  
后端需要发送一个 HTTP 请求到验证码系统来验证 token。  
- 验证接口 URL: `http://你的服务器IP:端口/api/verify_token`(可在环境变量中配置)
- 请求方法: `POST`
- 请求头:
  + `content-type`: `application/json` (**必须**，否则接口会响应 400)
- 载荷: 一个 JSON 字符串，包含要验证的 token。格式: `{"token": "xxxxxxxx"}`
- 响应: 一个 JSON 字符串，结构如下:
  |键|类型|说明|示例|
  |---|---|---|---|
  |retcode|integer|状态码|`0`: 成功查询(不代表token有效); `500`: 服务器内部错误;|
  |msg|string|消息|"OK"|
  |data|object|结果，格式为`{"result": 查询结果}`，查询结果为`true`代表 token 有效，否则 token 无效|{"result": true}|

Python 代码示例:  
```python
import requests
import json

def verify_token(token: str) -> bool:
    response = requests.post("http://你的服务器IP:端口/api/verify_token", headers={"content-type": "application/json"}, data=json.dumps({"token": token}))
    response = json.loads(response.text)
    if response["retcode"]:
        raise RuntimeError("查询失败")
    return response["data"]["result"]
```
**注意：此接口仅能在后端调用，严禁在前端调用，在前端调用是没有防护效果的！**
# 故障排除
1. 如果容器始终处于 unhealthy 状态，请查看日志目录中的 `error.log` 来了解报错原因。如果你无法确定原因，请带上 `error.log` [创建一个 Issue](https://github.com/Saobby/SaobbyCAPTCHA-V3/issues) 来报告问题。
# TODO
1. 支持自定义主题色、样式等
# 贡献
本项目欢迎贡献，请注意本项目的编码风格规范:  
- 使用双引号而不是单引号包裹字符串常量
- 使用 4 个空格缩进
- 使用小写字母+下划线的格式命名变量和函数，使用首字母大写无下划线的格式命名类  
如果你对本项目有任何建议，也欢迎在 [Issue](https://github.com/Saobby/SaobbyCAPTCHA-V3/issues) 提出！
# 第三方许可证
本项目的源码中包含了以下第三方项目的内容，它们的许可证可以在本仓库`/third_party_licenses`中找到。
- [tabler-icons](https://github.com/tabler/tabler-icons)
