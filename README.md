# 🎓 Internship Aggregator

[![React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react&logoColor=white)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind--CSS-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

[English] | [简体中文](./README.zh-CN.md)

A powerful full-stack internship aggregation platform designed to help students find, filter, and track their dream internships. Specifically optimized for Summer 2026 internship cycles.

---

## 📖 Project Overview

**Internship Aggregator** is a modern web application that solves the problem of scattered internship information. It automatically collects listings from trusted sources, processes them with intelligent tagging, and presents them in a clean, searchable interface.

Whether you're looking for AI/ML specific roles or need to know if a company is friendly to international students (H1B/Visa support), this tool provides the insights you need at a glance.

## 🚀 Core Features

- 🕷️ **Automated Crawler**: Real-time synchronization with high-quality internship repositories.
- 🔍 **Advanced Filtering**: Search by company, role, location, or industry with instant results.
- 🤖 **AI-Role Highlighting**: Automatically identifies and tags roles related to Artificial Intelligence and Machine Learning.
- 🌍 **International Student Focus**: Includes a "Friendliness Score" (1-10) to indicate visa sponsorship likelihood.
- ⚡ **Minimalist UI**: Responsive design built with Tailwind CSS for a seamless desktop and mobile experience.
- 📊 **One-Click Apply**: Direct links to application pages to save you time.

## 📂 Data Sources

The primary data source is the community-driven [SimplifyJobs/Summer2026-Internships](https://github.com/SimplifyJobs/Summer2026-Internships). 

The crawler is designed to be modular. It fetches the raw markdown data, parses the company details, roles, and locations, and enriches the data with:
- **International Friendliness Logic**: Based on metadata and historical sponsorship data.
- **AI Tagging**: Keyword-based detection in role descriptions.

## 🛠️ Tech Stack

- **Frontend**: React (Vite), Tailwind CSS, Lucide Icons.
- **Backend**: FastAPI (Python), SQLModel (ORM), Uvicorn.
- **Database**: SQLite (local storage for easy setup).
- **Automation**: Custom BeautifulSoup/Requests-based crawler.

## ⚙️ Getting Started

### 1. Backend Setup
```bash
# Clone the repository
git clone https://github.com/Mikelee2022/internship-aggregator
cd internship-aggregator

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Seed the database (optional)
python backend/crawler.py

# Start the server
uvicorn backend.main:app --reload
```
- API: `http://127.0.0.1:8000`
- Docs: `http://127.0.0.1:8000/docs`

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
- App: `http://localhost:5173`

## 📁 Project Structure
```text
internship-aggregator/
├── backend/            # FastAPI & Crawler logic
│   ├── main.py         # Entry point
│   ├── models.py       # SQLModel definitions
│   └── crawler.py      # Scraper implementation
├── frontend/           # React App
│   └── src/            # Components & Logic
└── README.md
```

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License.
