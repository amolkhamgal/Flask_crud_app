# Flask Notes Application

A simple Flask web application for user registration, login, and note management.

## Features

- User registration and login
- Create, read, update, and delete notes
- User authentication and session management

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- Werkzeug

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/your_project.git
   cd your_project
2. create vertual environment:
 python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate

4. pip install -r requirements.txt

4.Set up the database:
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

5. Run the application:
python app.py

6.Access the application:
Open your browser and go to http://127.0.0.1:5000

7. Usage
Register: http://127.0.0.1:5000/register
Login: http://127.0.0.1:5000/login
Dashboard: View, create, edit, and delete notes.
