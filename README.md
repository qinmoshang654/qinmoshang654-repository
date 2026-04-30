# 高珩博的个人主页

个人主页 + 数字分身聊天。基于 Flask + DeepSeek V4，带作品展示、随机提问、一键分享。

---

## 功能

-  个人信息展示（头像、标签、作品卡、联系方式）
-  数字分身聊天（接入 AI，语气模仿本人真实说话风格）
-  随机提问（不知道聊什么时点一下）
-  一键分享（复制链接发给朋友）
-  手机端自适应

---

## 技术栈

Python · Flask · DeepSeek API · 原生 HTML / CSS / JavaScript

---

## 本地运行

```bash
# 1. 克隆仓库
git clone <你的仓库地址>
cd gaohengbo-homepage

# 2. 安装依赖
pip install -r requirements.txt

# 3. 创建 .env 文件，写入你的 DeepSeek API Key
echo DEEPSEEK_API_KEY=你的Key > .env

# 4. 启动
python app.py
```

浏览器打开 `http://localhost:5000`

---

## 部署

推荐 [Vercel](https://vercel.com) 或 [Railway](https://railway.app)，免费额度够用。

部署时在平台后台设置环境变量：

```
DEEPSEEK_API_KEY=你的Key
```

不要上传 `.env` 文件。
