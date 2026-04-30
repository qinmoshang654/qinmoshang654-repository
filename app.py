"""
高珩博个人主页 — 后端服务
=============================

提供页面渲染和 AI 聊天代理。

- ``/`` — 渲染主页（templates/index.html）
- ``/api/chat`` — 接收前端消息，转发到 DeepSeek API，返回回复

环境变量:
    DEEPSEEK_API_KEY    DeepSeek API 密钥（必须）
"""

from flask import Flask, render_template, request, jsonify
import requests
import os

# ---------------------------------------------------------------------------
# 本地开发：从 .env 文件加载环境变量（部署时由平台设置，跳过此步）
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ---------------------------------------------------------------------------
# 应用初始化
# ---------------------------------------------------------------------------
app = Flask(__name__)

# DeepSeek API 配置（密钥通过环境变量注入，不写入代码）
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"


# ---------------------------------------------------------------------------
# 路由：主页
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """返回个人主页 HTML。"""
    return render_template("index.html")


# ---------------------------------------------------------------------------
# 路由：聊天 API
# ---------------------------------------------------------------------------
@app.route("/api/chat", methods=["POST"])
def chat():
    """
    接收前端对话记录，转发至 DeepSeek，返回模型回复。

    请求体 JSON:
        {
            "messages": [
                {"role": "system", "content": "..."},
                {"role": "user",   "content": "..."}
            ]
        }

    成功响应:
        {"content": "模型的回复文本"}

    失败响应:
        {"error": "错误描述"}, HTTP 500/504
    """
    data = request.get_json()
    messages = data.get("messages", [])

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "temperature": 0.8,
        "max_tokens": 200,
    }

    try:
        resp = requests.post(
            DEEPSEEK_ENDPOINT,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            },
            timeout=30,
        )
        resp.raise_for_status()
        resp_data = resp.json()

        # API 层错误
        if resp_data.get("error"):
            return jsonify({"error": resp_data["error"].get("message", "API error")}), 500

        # 提取回复内容
        content = None
        choices = resp_data.get("choices", [])
        if choices:
            content = choices[0].get("message", {}).get("content")

        if not content:
            return jsonify({"error": "empty response"}), 500

        return jsonify({"content": content})

    except requests.exceptions.Timeout:
        return jsonify({"error": "request timeout"}), 504

    except requests.exceptions.RequestException as exc:
        return jsonify({"error": str(exc)}), 500


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
