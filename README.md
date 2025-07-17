# 🛡️ AI Threat Analyst Bot

An intelligent cybersecurity assistant that integrates with SIEM tools like Splunk and ELK, detects anomalies using machine learning, and auto-generates threat reports using GPT-4. It provides real-time alerts via Slack and Email and includes a React dashboard for visualizing security insights.

---

## 🚀 Features

- ✅ Live SIEM Integration (Splunk, ELK)
- 🔍 AI-powered anomaly detection (Isolation Forest)
- 📊 GPT-4-based threat report generator
- 📬 Slack & Email alerting
- 🖥️ Simple, clean React-based UI
- ⏰ Scheduled background fetching with APScheduler

---

## 🔧 Tech Stack

- **Backend:** Flask, Scikit-learn, OpenAI API, APScheduler
- **Frontend:** React, Axios, Bootstrap
- **Alerts:** Slack SDK, SMTP
- **Data Sources:** Splunk, ElasticSearch

---

## 🛠️ Setup

### 1. Backend (Flask)
```bash
cd backend
pip install -r requirements.txt
python app.py
