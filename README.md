# 🏥 Healthcare Management System

A comprehensive Full-Stack Healthcare Management platform built with **Django**. This system is designed to digitize hospital workflows, including patient registrations, doctor scheduling, and pharmacy inventory management.

## 🌟 Key Features
* **User Authentication:** Secure login and registration for different user roles via the `accounts` module.
* **Appointment Scheduling:** Full management of patient-doctor consultations.
* **Doctor & Patient Records:** Centralized database for managing medical professionals and patient history.
* **Pharmacy Management:** Inventory tracking for medicines and prescriptions.
* **Interactive Dashboard:** A unified `healthcare_dashboard` for a quick overview of hospital metrics.
* **Deployment Ready:** Includes `Procfile` and `runtime.txt` for cloud hosting (e.g., Heroku).

## 🛠️ Tech Stack
* **Backend:** Python, Django
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
* **Database:** SQLite3 (Development)
* **Deployment:** Heroku/Cloud ready

## 📂 Project Structure
Based on the repository layout:
* `/accounts`: User authentication and profile management.
* `/appointments`: Scheduling and booking logic.
* `/doctors` & `/patients`: Specialized modules for medical staff and patient data.
* `/pharmacy`: Medicine stock and inventory control.
* `/healthcare_dashboard`: Main UI for hospital administration.
* `/static` & `/templates`: Global assets and UI components.

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ajay160380/Healthcare_project.git](https://github.com/ajay160380/Healthcare_project.git)
   cd Healthcare_project


   Set up Virtual Environment:

2. **Set up Virtual Environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```


3. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


4. **Database Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate

```


5. **Run the Application:**
```bash
python manage.py runserver

```


*Visit `http://127.0.0.1:8000/` in your browser.*

## 📄 License

This project is for educational purposes as part of my B.Tech CSE (AI) portfolio.

