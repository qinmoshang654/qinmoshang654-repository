from flask import Flask, render_template, request, jsonify, Response
import requests
import os

# 本地开发时自动加载 .env 文件
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
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
                "Authorization": "Bearer " + DEEPSEEK_API_KEY,
            },
            timeout=30,
        )
        resp_data = resp.json()

        if resp_data.get("error"):
            return jsonify({"error": resp_data["error"].get("message", "API error")}), 500

        content = None
        choices = resp_data.get("choices", [])
        if choices:
            content = choices[0].get("message", {}).get("content")

        if not content:
            return jsonify({"error": "empty response"}), 500

        return jsonify({"content": content})

    except requests.exceptions.Timeout:
        return jsonify({"error": "request timeout"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
