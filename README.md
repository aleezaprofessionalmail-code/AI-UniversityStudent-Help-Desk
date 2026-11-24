# AI University Student Help Desk 🎓

An AI-powered student help desk system designed to assist students with university-related queries and manage support tickets.

## Features

- Student registration and login
- Role-based Admin and Student dashboards
- AI-powered chatbot using TF-IDF
- Automatic query matching with a university FAQ dataset
- Support ticket creation and management
- Ticket status and department tracking
- SQLite database integration
- Password hashing for user accounts

## Tech Stack

- Python
- Flask
- HTML, CSS, JavaScript
- SQLite
- Pandas
- Scikit-learn
- TF-IDF
- Joblib

## Project Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/aleezaprofessionalmail-code/AI-UniversityStudent-Help-Desk.git
   cd AI-UniversityStudent-Help-Desk
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate it on Windows:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root and configure:

   ```env
   SECRET_KEY=your-own-secret-key
   ```

6. Run the application:

   ```bash
   python app.py
   ```

7. Open:

   http://127.0.0.1:5000/login

## Demo Credentials

**Admin**
- Username: `admin`
- Password: `123`

**Student**
- Username: `student`
- Password: `123`

These are demonstration credentials only. Do not use them in production.

## Dataset

The project includes a dataset of general university-related student questions, departments, solutions, and priorities.

## Developer

Aleeza Khan

Software Engineering Student | AI & Full Stack Developer

## License

This project is available for educational and learning purposes.
