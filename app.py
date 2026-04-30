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
import json
from datetime import datetime

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

# 日志查看密码（默认 gaobo2024，可通过环境变量 ADMIN_PASS 修改）
LOG_FILE = os.path.join(os.path.dirname(__file__), "chat_log.json")
ADMIN_PASS = os.getenv("ADMIN_PASS", "gaobo2024")


# ---------------------------------------------------------------------------
# 工具：记录对话到 JSON 文件
# ---------------------------------------------------------------------------
def log_chat(user_message, bot_reply):
    """将单次对话追加写入 chat_log.json。"""
    entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_message,
        "bot": bot_reply,
    }

    try:
        # 读取已有记录
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(entry)

    # 只保留最近 500 条
    if len(logs) > 500:
        logs = logs[-500:]

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# 路由：查看聊天日志（需密码）
# ---------------------------------------------------------------------------
@app.route("/admin/logs")
def admin_logs():
    """显示最近的聊天记录；需要 password 参数。"""
    password = request.args.get("pass", "")
    if password != ADMIN_PASS:
        return """
        <h2>需要密码</h2>
        <form method="get">
          <input type="password" name="pass" placeholder="输入密码">
          <button type="submit">查看</button>
        </form>
        """

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    # 最新在前
    logs = list(reversed(logs))

    html = """<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
      body { font-family: sans-serif; background: #fdfbf9; padding: 20px; color: #333; }
      .log { background: #fff; border: 1px solid #e8e0d7; border-radius: 10px; padding: 14px; margin-bottom: 10px; }
      .time { font-size: 12px; color: #999; margin-bottom: 6px; }
      .q { color: #2b4a6e; font-weight: 600; margin-bottom: 4px; }
      .a { color: #555; }
    </style>
    <h2>聊天记录（最近 {} 条）</h2>
    """.format(len(logs))

    for entry in logs:
        html += '<div class="log"><div class="time">{}</div><div class="q">Q: {}</div><div class="a">A: {}</div></div>'.format(
            entry["time"], entry["user"], entry["bot"]
        )

    return html


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

        # 记下这次对话
        log_chat(messages[-1].get("content", ""), content)

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
