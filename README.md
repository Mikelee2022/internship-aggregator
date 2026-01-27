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

## 📂 Rich Data Ecosystem

The core competency of the Internship Aggregator lies in its **unparalleled data richness**. Unlike other platforms that rely on a single source, we aggregate high-quality listings from a diverse network of sources, ensuring you never miss an opportunity.

### 🌟 Primary Data Sources

We currently track over **10+ premium sources** with specialized data collectors for each:

| Source Type | Source Name | Update Frequency | Description |
|-------------|-------------|------------------|-------------|
| **Community** | [SimplifyJobs GitHub](https://github.com/SimplifyJobs/Summer2026-Internships) | **Real-time** | The largest community-driven internship repository. |
| **Official** | **NASA** | Daily | Direct from `intern.nasa.gov`. Verified US Citizen roles. |
| **Official** | **Google** | Daily | Software, Product, and UX roles from `careers.google.com`. |
| **Official** | **Apple** | Daily | Hardware & Software engineering roles from `jobs.apple.com`. |
| **Official** | **Meta** | Daily | Research & Engineering roles from `metacareers.com`. |
| **Official** | **Microsoft** | Daily | PM & Engineering roles from `careers.microsoft.com`. |
| **Official** | **Goldman Sachs** | Daily | Finance & Tech roles from `goldmansachs.com`. |
| **Official** | **JPMorgan Chase** | Daily | SEP & Analyst programs from `careers.jpmorgan.com`. |
| **Official** | **Morgan Stanley** | Daily | Banking & Tech roles from `morganstanley.com`. |
| **Official** | **BlackRock** | Daily | Fintech & Analyst roles from `careers.blackrock.com`. |

### ⚙️ Extensible Collector Architecture

Our data collection engine is built for scale and flexibility:

- **Configurable Data Sources**: All sources are defined in `backend/data_sources.json`, allowing for easy additions without code changes.
- **Specialized Collectors**: Each source type (e.g., `github_readme`, `simulated_company_listing`) has a dedicated collector to handle its specific HTML structure and data format.
- **Intelligent Parsing**: We don't just scrape links; we extract metadata, detect visa sponsorship, and categorize roles using NLP heuristics.

## 🛠️ Tech Stack

- **Frontend**: React (Vite), Tailwind CSS, Lucide Icons.
- **Backend**: FastAPI (Python), SQLModel (ORM), Uvicorn.
- **Database**: SQLite (local storage for easy setup).
- **Automation**: Custom BeautifulSoup/Requests-based crawler.

## ⚙️ Getting Started

### 1. Backend Setup
```bash
# Clone the repositoryx`
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
