# LogWizard - Log Files Management Application

## Overview
LogWizard is a powerful log file management application designed to analyze, store, and visualize log data efficiently. It provides insightful analytics, error detection, and summarization using Google Gemini AI.

## Features
- **Log File Storage & Management**: Upload, store, and organize log files.
- **Error Detection & Analysis**: Identify and categorize errors from log files.
- **AI-Powered Summarization**: Uses Google Gemini API to extract key information and summarize log data.
- **Interactive Dashboards**: View error statistics and system activity through dynamic charts.
- **User Authentication**: Secure login and role-based access (Admin & User).
- **Notifications**: Get alerts based on log file activity and errors.

## Technologies Used
- **Backend**: Django (Python)
- **Database**: SQLite (default, adaptable to PostgreSQL/MySQL)
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **JavaScript Libraries**: jQuery, Chartist.js (for data visualization)
- **AI Integration**: Google Gemini API (for log file summarization)

## Installation
### Prerequisites
- Python 3.x
- Django
- SQLite/PostgreSQL/MySQL
- Bootstrap, jQuery, Chartist.js
- Google Gemini API Key

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/berrahokhalil/Logwizard
   cd Logwizard
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database:
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```
5. Access the application at:
   ```
   http://127.0.0.1:8000/
   ```

## Usage
   1. **Login/Register**: Create an account or log in.
   2. **Upload Logs**: Upload log files for processing.
   3. **View Statistics**: Analyze log files with interactive charts.
   4. **AI Summarization**: Get key insights via Google Gemini AI.
   5. **Manage Errors**: View error details and prioritize urgent issues.




