# 📈 Portfolio Insights

A stock analysis and alerting tool that lets users search for stock data and create custom price alerts. Built with a modern, scalable backend and a clean, reactive frontend.

---

## 🧠 Project Overview

**Portfolio Insights** lets users:

- Search for stock price history by ticker symbol
- Visualize recent price trends in a dynamic chart
- Create alerts for when a stock goes _above_ or _below_ a custom price
- View, search, and delete alerts with a responsive UI

---

## 🛠️ Tech Stack

| Layer    | Tools & Libraries                                          |
| -------- | ---------------------------------------------------------- |
| Frontend | React (Vite), Recharts, Vanilla CSS, AWS Amplify           |
| Backend  | FastAPI, psycopg, PostgreSQL (AWS RDS), yfinance, Docker   |
| DevOps   | GitHub Actions, Docker, AWS EC2, CI/CD, Husky, lint-staged |
| Linting  | ESLint, Prettier, Black                                    |

---

## 🚀 Features

- 🔍 Real-time ticker search with validation
- 📉 Historical price chart
- 🔔 Create stock alerts (above/below price)
- 🔄 Live refresh of alert display
- 🧼 Fully integrated linting/formatting workflow
- 🧪 Dual health check endpoints (`/health`, `/health/deep`)

---

## 📦 Local Development

**Backend:**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev server.py
```

** Frontend:**

```bash
cd frontend
npm install
npm run dev
```

Set environment variables in .env:

```env
VITE_API_URL=http://localhost:8000
```

## 🧪 CI/CD & Deployment

- Frontend deployed via AWS Amplify with auto-deploy from GitHub
- Backend runs in Docker on AWS EC2, built via GitHub Actions
- Database hosted on AWS RDS
- Pre-commit enforcement using Husky, Black, and Prettier
- Health monitored via dedicated endpoints

🔍 Demo
https://portfolio-insights.jakubstetz.dev

API exposed at https://api.portfolio-insights.jakubstetz.dev

📄 License
MIT License
