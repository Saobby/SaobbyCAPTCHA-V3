# SaobbyCAPTCHA-V3

一个基于汉字点选的简单易用、可配置的人机验证系统。  

---

## 系统要求

- **操作系统**:
  
  - 仅支持 Linux

- **运行环境**：  
  
  - Docker
  - Redis ≥ 6.0  

---

## 预览

https://github.com/user-attachments/assets/682f324c-f08e-4ade-834f-b3d34c1d2b94

[在线体验](https://captcha-v3.saobby.com/)  

---

## 功能亮点

- **用户友好**: 在完成一次验证码后，后几次可以不用再完成。

- **预生成验证码**：空闲时自动生成备用图片，应对可能突然出现高并发场景。  

- **速率限制**：拦截高频访问，对可疑用户强制验证。  

- **灵活配置**：支持自定义背景图、字体、验证码有效期等。  

- **轻量集成**：提供前端 JS 脚本与后端验证接口，快速嵌入业务系统。  

---

## 快速开始

### 1. 准备资源文件

```bash
# 创建背景图、字体和日志目录  
mkdir -p captcha/{backgrounds,fonts,log}  
# 创建词语列表
touch captcha/words.txt  

# 示例：添加词语（2~5 个汉字）  
echo -e "验证码\n网络安全\n人工智能" > captcha/words.txt  
```

- **背景图**：将一些 `.jpg/.png` 文件放入 `captcha/backgrounds`（建议尺寸 300px×225px，不是这个尺寸将会被强制缩放为这个尺寸）。  
- **字体**：将几个 `.ttf` 文件放入 `captcha/fonts`。  
- **词语**: 将一些 2~5 个字的词语放入 `captcha/words.txt`。
  
  
  
  在生成验证码时，会随机选择词语、背景图和字体。

### 2. 使用 Docker 部署

```bash
docker run -d \  
  -p 8080:5000 \  
  -v /path/to/captcha/backgrounds:/app/backgrounds \  
  -v /path/to/captcha/fonts:/app/fonts \  
  -v /path/to/captcha/log:/app/log \  
  -v /path/to/captcha/words.txt:/app/words.txt \  
  -e REDIS_HOST=127.0.0.1 \  
  -e REDIS_PORT=6379 \  
  -e API_VERIFY_TOKEN_PATH=/api/your_secret_verify \  
  -e REAL_IP_HEADER= \  
  --restart=unless-stopped \  
  axolotltech/saobby-captcha-v3:latest  
```

**安全提示**：  

- 强烈建议通过 Nginx 配置 HTTPS 反向代理，避免 Token 明文传输，还能对响应进行压缩。

- 设置 `API_VERIFY_TOKEN_PATH` 为复杂路径（如 `/api/your_secret_verify`），防止 token 验证接口暴露。  

**状态监控**:

- 使用 `docker ps` 检查容器状态，如果为 `healthy` 则启动成功，如果一直是 `unhealthy`，请查看故障排除章节。

- 如果使用了反向代理，查看 `captcha/log/access.log` 检查入站 IP 以确认 `REAL_IP_HEADER` 是否配置正确。

## 详细配置

### 关键环境变量

| 键                       | 说明                                                                                              | 默认值               |
| ----------------------- | ----------------------------------------------------------------------------------------------- | ----------------- |
| `REDIS_HOST`            | Redis 服务地址，可以是 IP 或域名                                                                           | 127.0.0.1         |
| `REDIS_PORT`            | Redis 端口                                                                                        | 6379              |
| `API_VERIFY_TOKEN_PATH` | 设置你的网站后端用于校验 token 的 API 的访问路径。由于本接口没有速率限制，应尽量避免外部访问，**因此请设置一个其他人猜不到的路径。**                      | /api/verify_token |
| `REAL_IP_HEADER`        | 用于获取用户真实 IP 的请求头(比如 `x-forwarded-for`)，留空则使用网络连接中的 IP。**<u>如果使用了 Nginx 做反向代理，请务必正确设置此项！！！</u>** |                   |
| `IMAGE_POOL_SIZE`       | 预生成验证码图片池大小（设为 `0` 禁用图片预生成）                                                                     | 500               |
| `RATE_LIMIT_MAX_AMOUNT` | 10 秒内允许的最大请求次数，超出触发验证码强制验证                                                                      | 10                |
| `BYPASS_TIMES`          | 成功验证后，后续多少次请求可跳过验证                                                                              | 5                 |
| `TOKEN_EXPIRATION_TIME` | Token 有效期（单位：秒），建议 ≤ 300                                                                        | 120               |

<details>
  <summary>展开完整环境变量配置</summary>

  |键|描述|默认值|
  |---|---|---|
  |`REDIS_HOST`|Redis 服务地址，可以是 IP 或域名|127.0.0.1|
  |`REDIS_PORT`|Redis 端口|6379|
  |`REDIS_USERNAME`|Redis 用户名(如果没有设置请留空)| |
  |`REDIS_PASSWORD`|Redis 访问密码(如果没有设置请留空)| |
  |`REDIS_RETRY_ON_TIMEOUT`|Redis 请求超时时，是否重试|true|
  |`REDIS_MAX_CONNECTIONS`|Redis 连接池的最大连接数|1024|
  |`REDIS_PREFIX`|程序向 Redis 中存储内容时键的前缀(如果多个本验证码系统依赖同一个 Redis 实例，请设置不同的前缀)|saobby_captcha_|
  |`REAL_IP_HEADER`|用于获取用户真实 IP 的请求头(比如 `x-forwarded-for`)，留空则使用网络连接中的 IP。**<u>如果使用了 Nginx 做反向代理，请务必正确设置此项！！！</u>**| |
  |`CORS_ORIGIN`|设置响应头中 Access-Control-Allow-Origin 的值。如果设置为 * , 则会赋值为请求头中 Origin 的值(老旧浏览器不支持通配符)|*|
  |`API_VERIFY_TOKEN_PATH`|设置你的网站后端用于校验 token 的 API 的访问路径。由于本接口没有速率限制，应尽量避免外部访问，**因此请设置一个其他人猜不到的路径。**|/api/verify_token|
  |`ENABLE_TEST_PAGE`|设置是否启用测试页面，启用后，在访问根路径时会显示一个测试页面|true|
  |`IMAGE_POOL_SIZE`|预生成验证码图片池大小（设为 `0` 禁用图片预生成）|500|
  |`CHALLENGE_EXPIRATION_TIME`|验证码的完成时限(单位: s)|300|
  |`TOKEN_EXPIRATION_TIME`|验证码完成后获得的 token 的有效期(单位: s)(不建议设置太长)|120|
  |`RATE_LIMIT_TIME_INTERVAL`|速率限制的测速区间(单位: s)|10|
  |`RATE_LIMIT_MAX_AMOUNT`|在 1 个测速区间内，最多访问的次数|10|
  |`RATE_LIMIT_ENABLE_PENALTY`|达到速率限制时，是否强制每次都需要完成验证码。|true|
  |`RATE_LIMIT_BAN_DURATION`|达到速率限制的惩罚的有效时间(单位: s)|14400 (4 小时)|
  |`BYPASS_TIMES`|完成一个验证码后，后面的多少次可以不用再完成|5|
  |`BYPASS_EXPIRATION_TIME`|完成一个验证码后，后面几次可不用再完成的效果的有效期(单位: s)(不建议设置太长)|300|
  |`TIP_FONT_SIZE`|提示文本图片的字体大小|30|
  |`CHALLENGE_FONT_SIZE`|验证码图片中文字的大小|45|
  |`TIP_MAX_ROTATE_ANGLE`|提示文本图片的字体最大旋转角度|20|
  |`CHALLENGE_MAX_ROTATE_ANGLE`|验证码图片的字体最大旋转角度|45|
  |`BACKGROUND_IMAGES_DIR`|容器内存放背景图片的目录，不建议修改，直接修改绑定宿主机的目录即可。|./backgrounds|
  |`FONTS_DIR`|存放字体的目录，不建议修改，直接修改绑定宿主机的目录即可。|./fonts|
  |`WORDS_PATH`|存放词汇列表(一行一个)的文本文件(UTF-8编码)，不建议修改，直接修改绑定宿主机的目录即可。|./words.txt|
  |`DO_INIT`|程序启动时，是否进行初始化操作。初始化操作包括:将所有背景图片缩放到所需要的尺寸，并转换为 jpg 格式(不会重复转换);开始填充图片池; 不建议修改。|true|
  |`GUNICORN_PORT`|容器内监听的端口。不建议修改，直接修改容器端口映射即可。|5000|
  |`GUNICORN_LOG_LEVEL`|Gunicorn 日志级别。不建议修改。|warning|
  |`LOGS_DIR`|容器内访问日志和错误日志的存放目录，不建议修改，直接修改绑定宿主机的目录即可。|./log|
</details>

---

## 前端集成

在后端部署完成后，您需要在前端页面中引入验证码的 JavaScript 文件。该文件可以从以下路径获取：

```html
<script src="https://你的域名/static/js/saobbyCaptchaV3.js"></script>
```

请将 `你的域名` 替换为您实际部署验证码服务的域名。引入此脚本后，您就可以在页面中使用 `SaobbyCaptchaV3` 类来集成人机验证功能。

### 方式 1：表单自动嵌入

```html
<form method="post" action="/login">  
  <input type="text" name="username">  
  <input type="password" name="password">  
  <!-- 验证码容器 -->  
  <div id="captcha-container"></div>  
  <script>  
    const captcha = new SaobbyCaptchaV3({  
      apiBaseUrl: "https://your-site.com",  // 建议使用 HTTPS  
      showTrigger: true,                    // 显示"点击进行人机验证"的框
      container: document.getElementById("captcha-container")  
    });  
  </script>  
  <button type="submit">登录</button>  
</form>  
```

这种方式会在网页表单上自动附带上一个 `SCV3_token` 参数，包含人机验证 token，以供后端验证。

### 方式 2：手动触发验证

```javascript
const captcha = new SaobbyCaptchaV3({  
  apiBaseUrl: "https://your-site.com",  
  showTrigger: false  
});  

// 在需要时调用  
document.getElementById("submit-btn").onclick = async () => {  
  const result = await captcha.verify();  
  if (result.retcode === 0) {  
    console.log("Token:", result.data.token);  
  }  
};  
```

这种方式更加灵活，但是需要前端手动将 token 发送给后端。

### 详细文档

<details>
  <summary>点击展开前端接口详细说明</summary>

  `SaobbyCaptchaV3` 是一个类，包含以下几个方法:  
  
  - `constructor(options)` (创建对象)  
    `options` 是一个 `object`，有以下几个键:
      |键|数据类型|是否必须|说明|默认值|
      |---|---|---|---|---|
      |`apiBaseUrl`|string|是|验证码系统的公网访问地址，比如`https://captcha.your-site.com`(末尾没有`/`)。**强烈建议再使用 nginx 反向代理本验证码服务，以便对响应进行压缩和配置 SSL 证书**|无|
      |`showTrigger`|bool|否|是否显示"点击进行人机验证"的框框|false|
      |`container`|DOM 元素|否|设置验证码组件要放在哪个元素内(见示例)。如果设置了`showTrigger`为`true`则此项必须指定。|如果不指定会自动创建一个`div`标签用于放置组件|
      |`once`|bool|否|在验证完一次后，是否销毁人机验证对象。如果设置了`showTrigger`为`true`则不能设置本项为`true`|false|
  
  - `verify()`  
    返回一个 `Promise`。调用时会进行人机验证，并返回结果。  
    这个 `Promise` 只会 resolve。  
    返回的结果是一个 `object`，结构如下:  
    |键|数据类型|说明|示例|
    |---|---|---|---|
    |`retcode`|integer|验证结果的类型|`0`: 验证成功; `1`: 用户点了×关闭验证窗口; `429`: 请求过于频繁; `500`: 服务器内部错误; `-1`: 网络错误;|
    |`msg`|string|错误消息|"用户取消了验证"|
    |`data`|object|验证结果的数据值,如果验证成功,其中会包含验证码 token, 格式为`{token: "验证码 token"}`|{token: "xxxxxxxx"}|
  
  - `destroy()`  
    手动将验证码的 HTML 从 DOM 中移除，此操作不可逆，移除后无法再使用验证功能，需要重新创建验证码对象。
</details>

---

## 后端验证示例（Python）

```python
import requests
import json

def verify_token(token: str) -> bool:
    url = "https://your-site.com/api/your_secret_verify"  # 路径与环境变量 API_VERIFY_TOKEN_PATH 一致  
    response = requests.post(url, 
        headers={"content-type": "application/json"},   # 必须设置请求头，否则后端会响应 400
        data=json.dumps({"token": token})
    )
    response = json.loads(response.text)
    if response["retcode"]:
        raise RuntimeError("查询失败")
    return response["data"]["result"]
```

**注意**：此接口仅能在后端调用，严禁在前端调用，在前端调用是没有防护效果的！

### 详细文档

<details>
  <summary>点击展开后端接口详细说明</summary>

  - 验证接口 URL: `/api/verify_token`(可在环境变量中配置)
 
  - 请求方法: `POST`
  
  - 请求头:
    + `content-type`: `application/json` (**必须**，否则接口会响应 400)
  
  - 载荷: 一个 JSON 字符串，包含要验证的 token。格式: `{"token": "xxxxxxxx"}`
  
  - 响应: 一个 JSON 字符串，结构如下:
    |键|类型|说明|示例|
    |---|---|---|---|
    |`retcode`|integer|状态代码|`0`: 成功查询(不代表token有效); `500`: 服务器内部错误;|
    |`msg`|string|消息|"OK"|
    |`data`|object|结果，格式为`{"result": 查询结果}`，查询结果为`true`代表 token 有效，否则 token 无效|{"result": true}|
</details>

---

## 故障排查

### 常见问题

- **容器状态非 `healthy`**：  
  检查 `captcha/log/error.log`，常见报错：  
  
  - Redis 连接失败 → 检查是否正确设置 Redis 的地址和端口。  

  - 字体/图片加载失败 → 检查是否正确配置目录映射，并放入背景图片和字体

### 漏洞报告

请附带 `error.log` [创建一个 Issue](https://github.com/Saobby/SaobbyCAPTCHA-V3/issues) 来报告问题。

---

## 最佳实践

1. **性能优化**：  
   - 根据服务器内存调整 `IMAGE_POOL_SIZE`（每张验证码图片约占用 10KB）。  

2. **安全性**：  
   - 定期更新 `words.txt` 中的词汇。  

---

## 贡献指南

欢迎提交 Issue 或 PR！代码规范：  

- 变量命名：`lower_case_with_underscores`  

- 类命名：`UpperCamelCase`  

- 字符串：统一使用双引号  

- 缩进: 使用 4 个空格

---

## TODO

1. 支持自定义主题色、样式等

---

## 第三方许可证

本系统使用了以下第三方项目的资源，它们的许可证文件存放在仓库 `/third_party_licenses` 目录中：

| 项目名称                                                   | 用途      | 许可证类型 | 版本     |
| ------------------------------------------------------ | ------- | ----- | ------ |
| [tabler-icons](https://github.com/tabler/tabler-icons) | 验证码界面图标 | MIT   | 3.30.0 |
