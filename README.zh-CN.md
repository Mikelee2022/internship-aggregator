# 🎓 实习信息聚合器 (Internship Aggregator)

[![React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react&logoColor=white)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind--CSS-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

[English](./README.md) | [简体中文]

一个功能强大的全栈实习信息聚合平台，旨在帮助学生发现、筛选并追踪心仪的实习机会。特别针对 2026 年夏季实习周期进行了优化。

---

## 📖 项目概述

**Internship Aggregator** 是一个现代化的 Web 应用程序，解决了实习信息碎片化的问题。它能自动从可信源收集职位列表，通过智能标签进行处理，并在简洁、可搜索的界面中展示。

无论您是在寻找 AI/ML 特定职位，还是想了解公司对国际学生（H1B/签证支持）的友好程度，该工具都能为您提供一目了然的见解。

## 🚀 核心特性

- 🕷️ **自动化爬虫**：与高质量的实习仓库实时同步。
- 🔍 **高级筛选**：按公司、职位、地点或行业搜索，即时获取结果。
- 🤖 **AI 职位高亮**：自动识别并标记与人工智能和机器学习相关的职位。
- 🌍 **国际学生关注**：包含“友好度评分”（1-10），指示签证赞助的可能性。
- ⚡ **极简 UI**：基于 Tailwind CSS 的响应式设计，提供无缝的桌面和移动端体验。
- 📊 **一键申请**：直接跳转至申请页面，节省您的时间。

## 📂 数据来源

主要数据来源是社区驱动的 [SimplifyJobs/Summer2026-Internships](https://github.com/SimplifyJobs/Summer2026-Internships)。

爬虫采用模块化设计。它获取原始 Markdown 数据，解析公司详情、职位和地点，并丰富数据：
- **国际学生友好度逻辑**：基于元数据和历史赞助数据。
- **AI 标签**：基于职位描述中的关键词检测。

## 🛠️ 技术栈

- **前端**: React (Vite), Tailwind CSS, Lucide Icons.
- **后端**: FastAPI (Python), SQLModel (ORM), Uvicorn.
- **数据库**: SQLite (本地存储，易于配置)。
- **自动化**: 基于 BeautifulSoup/Requests 的自定义爬虫。

## ⚙️ 快速开始

### 1. 后端设置
```bash
# 克隆仓库
git clone https://github.com/Mikelee2022/internship-aggregator
cd internship-aggregator

# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r backend/requirements.txt

# 填充数据库（可选）
python backend/crawler.py

# 启动服务器
uvicorn backend.main:app --reload
```
- API 地址: `http://127.0.0.1:8000`
- 文档地址: `http://127.0.0.1:8000/docs`

### 2. 前端设置
```bash
cd frontend
npm install
npm run dev
```
- 应用地址: `http://localhost:5173`

## 📁 项目结构
```text
internship-aggregator/
├── backend/            # FastAPI & 爬虫逻辑
│   ├── main.py         # 入口文件
│   ├── models.py       # SQLModel 定义
│   └── crawler.py      # 爬虫实现
├── frontend/           # React 应用
│   └── src/            # 组件与逻辑
└── README.md
```

---

## 🤝 参与贡献
欢迎贡献！请随时提交 Pull Request。

## 📄 开源协议
本项目采用 MIT 协议。
