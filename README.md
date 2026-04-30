# 高珩博的个人主页

线上地址：**[qinmoshang.pythonanywhere.com](https://qinmoshang.pythonanywhere.com/)**

---

## 项目简介

个人主页 + 数字分身聊天。前端为原生 HTML/CSS/JS，后端为 Python Flask，聊天接口代理至 DeepSeek V4。

### 功能

| 模块 | 说明 |
|------|------|
| 个人信息 | 头像、标签、作品卡、联系方式 |
| 数字分身 | 接入 AI，语气模仿本人真实说话风格 |
| 随机提问 | 不知道聊什么时点一下，自动抽取问题 |
| 一键分享 | 复制链接发给朋友 |
| 响应式 | 桌面端双栏，手机端自动堆叠 |

---

## 技术栈

| 层 | 技术 |
|----|------|
| 后端 | Python 3.11+ · Flask |
| 前端 | 原生 HTML / CSS / JavaScript（无框架） |
| AI | DeepSeek API（`deepseek-chat`） |
| 部署 | PythonAnywhere（免费版） |

---

## 本地运行

```bash
# 1. 克隆仓库
git clone https://github.com/qinmoshang654/qinmoshang654-repository.git
cd qinmoshang654-repository

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 DEEPSEEK_API_KEY

# 4. 启动
python app.py
```

浏览器打开 `http://localhost:5000`

---

## 项目结构

```
.
├── app.py              # Flask 后端入口
├── requirements.txt    # Python 依赖
├── .env.example        # 环境变量模板（不含真实密钥）
├── .gitignore
├── runtime.txt         # PythonAnywhere 运行时声明
├── README.md
├── templates/
│   └── index.html      # 前端页面
└── static/
    ├── avatar.jpg      # 头像
    └── image.png       # 弹窗背景
```

---

## 部署

本项目部署在 PythonAnywhere（免费版）。

部署需要设置环境变量：

```
DEEPSEEK_API_KEY=你的密钥
```

不要将 `.env` 文件提交到 Git（已在 `.gitignore` 中排除）。
