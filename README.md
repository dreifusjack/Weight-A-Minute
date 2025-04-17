# Weight a Minute! – Spring 2025 CS 3200 Project

**Members:**

- Henry Caldwell (caldwell.h@northeastern.edu)
- Jack Dreifus (dreifus.j@northeastern.edu)
- Owen Sharpe (sharpe.o@northeastern.edu)
- Christopher Pyle (pyle.c@northeastern.edu)

---

## About

**Weight a Minute!** is a fitness platform that lets gym-goers, trainers, and gym owners track workouts, assign routines, manage equipment, and view analytics. It keeps everything centralized so that users have a one stop location to optimize their workouts.

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- (Optional) Python 3.9

---

## Environment Variables

Create a file at `./api/.env` with the following entries (replace values as needed):

```dotenv
SECRET_KEY=<your-secret-key>
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=weight-a-minute
MYSQL_ROOT_PASSWORD=<secret-root-password>
MAIL_USERNAME=<your-mail-username>
MAIL_PASSWORD=<your-mail-password>
```

---

## Setup & Deployment

1. Clone the Repo

2. Create your .env file

3. Start services

```bash
docker compose up -d
```

---

## Running the Application

To run the application open your browser to http://localhost:8501

You can now use Weight A Minute!

---

## Organization

### 1. Flask REST API (`/api`)
- **Blueprints** (in `backend/`):
  - `users` → `/u`  
  - `gyms` → `/g`  
  - `fitness` → `/f`  
  - `community` → `/c` 

### 2. Streamlit Frontend (`/app`)
- **Entry Point**  
  - `src/Home.py` sets up logging, "authentication" and loads the first page.
- **Navigation**  
  - `src/modules/nav.py` defines a common sidebar and links/logo.
- **Pages** (`src/pages/`):  
  - Each user persona (Admin, Owner, Trainer, User) has its own home and function pages, e.g.:  
    - `Admin_Home.py`, `Admin_View_Users.py`, 
    - `Owner_Home.py`, `Owner_Manage_Subscriptions.py` 
    - `Trainer_Manage_Workouts.py`, `Trainer_View_Client_Workouts.py` 
    - `User_Home.py`, `User_View_Leaderboard.py`
