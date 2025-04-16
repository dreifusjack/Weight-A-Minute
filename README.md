# Weight a Minute! – Spring 2025 CS 3200 Project

**Members:**  
- Henry Caldwell (caldwell.h@northeastern.edu)  
- Jack Dreifus (dreifus.j@northeastern.edu)  
- Owen Sharpe (sharpe.o@northeastern.edu)  
- Christopher Pyle (pyle.c@northeastern.edu)  

---

## About the Application 

We’re building **Weight a Minute!**, a fitness app that helps users track workouts, connect with trainers, and discover gyms that match their equipment needs. Because not every gym offers the same machines, generic plans often fall short—our app solves this by delivering customized workouts based on the exact equipment available at a user’s gym. Three main personas benefit:

1. **Gym‐goers:** Streamline workouts, track progress, and never waste time on unusable plans.  
2. **Trainers:** Engage clients asynchronously, assign routines, review performance, and post blog content.  
3. **Gym Owners:** Showcase facilities—upload location, equipment lists, memberships, photos, and promotions.

Key features:  
- Create, customize, and track workout routines  
- View trainer posts, tips, and faqs  
- Browse and sign up for gyms and even post you own

---

## Prerequisites

- Git
- VS Code
- Python 3.8+ (Anaconda/Miniconda recommended)  
- Docker 
- mySQL 

---

## Project Architecture

Each service runs in its own Docker container:

1. **Streamlit UI** (`./app`)  
   - Streamlit pages for user dashboards supporting 4 distint personas.
2. **Flask REST API** (`./api`)  
   - Endpoints for workouts, trainers, gyms, and users.  
3. **MySQL Database** (`./database-files`)  
   - Initialized via SQL scripts in `./database-files/db_csvs/` (users, workouts, gyms, equipment tables, etc.).

---

## Getting Started

1. **Clone & Explore**  
   - Fork this repo → clone locally → `cd weight-a-minute`  
2. **Streamlit App (`./app`)**  
   - Entry point: `app/src/Home.py`  
   - Check sidebar links & page routing in `app/src/nav.py`  
3. **Flask API (`./api`)**  
   - Main app: `api/backend/rest_entry.py`  
   - Routes organized under `api/backend/(blueprint_name)` (e.g. `workouts.py`, `trainers.py`)  
4. **Database (`./database-files`)**  
   - Tables in `01_WEIGHTAMINUTE DDL.sql`  
   - Seed data handled in `/db_csvs`
5. **IMPORTANT** (realize this is not secure but just for grading purposes) create an env file in `./api` directory following this format (Note MAIL_USERNAME and PASSWORD must match what is below): 
```
SECRET_KEY=someCrazyS3cR3T!Key.!
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=weight-a-minute
MYSQL_ROOT_PASSWORD= anything you want 
MAIL_USERNAME=adammin.weightaminute@gmail.com
MAIL_PASSWORD=xopdyhjlnkjhrlsp # app generated password
```

---

## Local Setup

### 1. Fork & Clone

- Fork this repo to your GitHub account.  
- Clone your fork:  
  ```bash
  git clone https://github.com/<your‑username>/weight-a-minute.git
  cd weight-a-minute
  ```
- Running the project:
  ```bash
  docker compose up
  ```
  Then navigate to http://localhost:8501/
