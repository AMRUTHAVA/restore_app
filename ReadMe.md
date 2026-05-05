# Restore Application – Local Setup Guide

This document explains the **project setup**, **required versions**, and **step‑by‑step instructions** to run the application on a **local machine**.

---

## Tech Stack & Versions

* **Backend Framework**: Django
* **Programming Language**: Python **3.12** (Recommended & Tested)
* **Database**: PostgreSQL
* **Package Manager**: pip
* **Virtual Environment**: venv

> ⚠️ Make sure **Python 3.12** is installed before proceeding. Other versions may cause dependency issues.

---

## 📂 Project Structure (Important Files)

```
project-root/
│── manage.py
│── requirements.txt
│── restore_db.sql   (if applicable)
│── .env             (environment variables)
│── app/
│── venv/
```

---

## Step 1: Install Python 3.12

### Ubuntu

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

### macOS (Homebrew)

```bash
brew install python@3.12
```

Verify installation:

```bash
python3.12 --version
```

---

## Step 2: Create Virtual Environment

From the **project root directory**:

```bash
python3.12 -m venv venv
```

### Activate Virtual Environment

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\\Scripts\\activate
```

Verify:

```bash
python --version
```

---

## Step 3: Install Dependencies

Make sure you are inside the virtual environment.

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ Step 4: Environment Variables

Create a `.env` file in the project root (if not present):

```env
DEBUG=True
SECRET_KEY=your-secret-key
DB_ENGINE=postgresql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASS=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

---

## Step 5: Database Setup

### Create Database (PostgreSQL)

```sql
CREATE DATABASE your_db_name;
```

### Restore Database (If applicable)

```bash
psql -U your_db_user -d your_db_name -f restore_db.sql
```

```bash
< PROJECT ROOT >
   |
   |-- config/                            
   |    |-- settings.py                  # Project Configuration  
   |    |-- urls.py                      # Project Routing
   |
   |-- apps/
   |    |-- restore  
   |     
   |-- requirements.txt                  # Project Dependencies
   |
   |-- env.sample                        # ENV Configuration (default values)
   |-- manage.py                         # Start the app - Django default start script
   |
   |-- ************************************************************************
```

---

## Step 6: Django Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

To verify migrations:

```bash
python manage.py showmigrations
```

---

## Step 7: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts:

* Username
* Email
* Password

Admin panel will be available at:

```
http://127.0.0.1:8000/admin/
```

---

## Step 8: Run the Application

```bash
python manage.py runserver
```

Application URLs:

* **Admin Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
* **UI Dashboard**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Useful Commands

```bash
# Check Django version
python -m django --version

# Collect static files (if needed)
python manage.py collectstatic

# Deactivate virtual environment
deactivate
```

---

## Common Issues & Fixes

### Migration issues after Python upgrade

 Ensure virtual environment is recreated using Python 3.12

### psycopg2 error

 Install system dependencies:

```bash
sudo apt install libpq-dev
```

---

## Status

✔ Django Admin Portal – Working
✔ UI Dashboard – Working
✔ Migrations – Applied Successfully


# AWS-deployment
We are deploying the 'develop' branch as staging environment

Here are the steps to follow:
1. https://us-east-1.console.aws.amazon.com/ec2-instance-connect/ssh/home?region=us-east-1&connType=standard&instanceId=i-052140174448abc90&osUser=ubuntu&sshPort=22&addressFamily=ipv4
 is the server instance login and go here.
2. Server's terminal will be opened here. 
3. when you push code to develop branch (Which means when the PR's are merged to develop branch new changes are pushed to develop branch)
4. Follow the below commands:
   ```bash
   $cd /home/ubuntu/restore-app
   $git pull origin develop
   $source venv/bin/activate
   $pip install -r requirements.txt
   $python manage.py migrate
   $python manage.py collectstatic --noinput
   $sudo systemctl restart gunicorn
   $sudo systemctl reload nginx
   ```
5. Make sure these below commands show the active running.
   ```bash
   $sudo systemctl status nginx
   $sudo systemctl status gunicorn
   ```
6. The Server will be restarted successfully.

## Server URLs:

### Staging Application URLs:

* **Admin Portal**: [http://44.200.47.254/admin/](http://44.200.47.254/admin/)
* **UI Dashboard**: [http://44.200.47.254/](http://44.200.47.254/)

