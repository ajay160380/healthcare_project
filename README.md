---
title: Healthcare Dashboard
emoji: 🏥
colorFrom: indigo
colorTo: emerald
sdk: docker
pinned: false
---

# 🏥 Advanced Healthcare Management Portal

Welcome to the **Advanced Healthcare Management Portal**—a full-stack, enterprise-grade hospital administration and assistant platform built with **Django 6.0** and **Python 3.12**. This portal digitizes critical hospital workflows, implements a modern theme overhaul, integrates a smart AI Health Assistant, and features a local emergency hospital map finder.

---

## 🚀 Live Demo & Deployment
Experience the live application deployed on Hugging Face Spaces:
👉 **[live demo](https://solocode12-healthcare.hf.space)**

---

## 🌟 Key Features

### 🎨 1. Premium Glassmorphic UI Overhaul
- **Modern Theme:** Implemented a sophisticated Indigo/Emerald/Rose color palette with custom CSS tokens.
- **Glassmorphic Cards:** Styled authentication pages (login, registration) with premium blur effects and hover states.
- **Responsive Layout:** Responsive sidebar navigation, custom badges, status indicators, and micro-interactions.

### 🤖 2. Smart AI Health Assistant
- **Core Engine:** Integrated the high-performance **Groq Llama-3.1** AI model (`llama-3.1-8b-instant`).
- **Interactive Chat Interface:** Features quick preset prompts, real-time response generation, and markdown-rendered responses.
- **Secure Key Loading:** Dynamically reads API keys from environment settings for production security.

### 📍 3. Interactive Emergency Hospital Finder (Lucknow)
- **Leaflet.js Map Integration:** Renders geolocation pins for primary hospitals in Lucknow.
- **Interactive Controls:** Center and focus maps automatically by clicking on hospital cards.
- **Emergency Telephony:** Instant dial shortcuts (`tel:`) for immediate medical assistance.

### 📋 4. Clinical & Inventory Modules
- **Patient Management:** Centrally track registrations, clinical history, and patient stats.
- **Doctor Scheduling:** Schedule and assign active doctors based on area specializations.
- **Pharmacy Inventory:** Keep track of medicine stock, expiration dates, low-stock warnings, and dispensing history.

---

## 🛠️ Tech Stack & Badges

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511F2.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-yellow?style=for-the-badge)

- **Backend:** Python 3.12, Django 6.0
- **Frontend:** HTML5, Vanilla CSS, JS, Leaflet.js
- **Database:** SQLite3 (Local development)
- **Deployment & Containers:** Docker, Hugging Face Spaces SDK

---

## 📂 Project Structure
```
├── accounts/               # User registration, profiles, AI Assistant & Maps views
├── appointments/           # Scheduling logic and patient-doctor booking views
├── doctors/                # Medical professionals, availability and specializations
├── patients/               # Patient databases, vitals and records
├── pharmacy/               # Medicine inventory, low-stock tracking and dispensing
├── healthcare_dashboard/   # Project configuration, settings, routing
├── templates/              # Base layouts and module-specific UI files
├── static/                 # Custom custom.css styling, fonts and assets
├── Dockerfile              # Docker container configurations for Hugging Face
├── requirements.txt        # Production Python dependencies
├── setup.py                # Database seed script for generating 500+ Lucknow doctors
└── manage.py               # Django administration utility
```

---

## ⚙️ Local Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ajay160380/healthcare_project.git
   cd healthcare_project
   ```

2. **Set up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your Groq API Key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Migrations & Seed Data:**
   Run migrations and execute the database seed script to populate 500+ doctors:
   ```bash
   python manage.py migrate
   python setup.py
   ```

6. **Run Server:**
   ```bash
   python manage.py runserver
   ```
   *Open `http://127.0.0.1:8000/` to access the application.*

---

## 🐳 Hugging Face Spaces Docker Deployment

The application is deployed using a custom Dockerfile configured for the Hugging Face Docker SDK.

### Key Deployment Characteristics:
- **Port:** Configured to listen on the default Hugging Face container port `7860`.
- **Security:** Excludes virtual environments and sensitive credentials via `.gitignore`.
- **Initialization:** Running the Docker container automatically triggers `python manage.py migrate` and runs `setup.py` to seed fresh doctor/appointment databases.
- **Environment API Config:** The `GROQ_API_KEY` is loaded dynamically from the environment. Add this key under **Space Settings > Variables and Secrets** to enable the AI Health Assistant.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details. Created as part of the B.Tech CSE (AI) portfolio.
