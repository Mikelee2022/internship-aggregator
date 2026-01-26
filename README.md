# Internship Aggregator MVP

A full-stack internship aggregation platform built with **React**, **Tailwind CSS**, and **FastAPI**.

**Repo**: [https://github.com/Mikelee2022/internship-aggregator](https://github.com/Mikelee2022/internship-aggregator)

## Features
- 🕷️ **Automated Crawler**: Scrapes internship listings (default source: GitHub).
- 🔍 **Search & Filter**: Filter by keyword, location, or industry.
- 🏷️ **AI Tags**: Automatically highlights AI/ML related roles.
- ⚡ **Modern UI**: Clean, responsive interface using Tailwind CSS.

## Prerequisites
- Python 3.8+
- Node.js 16+

## Quick Start

### 1. Backend Setup
Navigate to the root directory and run:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run the crawler to seed the database (optional, runs automatically on first start if configured, but good to run manually once)
python backend/crawler.py

# Start the API server
uvicorn backend.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.
Docs available at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup
Open a new terminal, navigate to the root directory:

```bash
cd frontend

# [x] Install dependencies
npm install

# [x] Start the development server
npm run dev
```
The application will be running at `http://localhost:5173`.

## Project Structure
```
internship-aggregator/
├── backend/
│   ├── main.py          # FastAPI app entry point
│   ├── models.py        # Database models
│   ├── database.py      # DB connection & session
│   ├── crawler.py       # Data scraping logic
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/  # React components (Card, Search)
│   │   ├── App.jsx      # Main application page
│   │   └── main.jsx
│   └── tailwind.config.js
└── README.md
```
