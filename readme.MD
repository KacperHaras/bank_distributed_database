# Distributed Database Bank Project

## Description
This Flask-based web application manages a distributed bank database system made for simulation of distributed bank database. 

## Features
- User authentication and account preview.
- Multiple branch database support.
- Real-time transaction processing and logging.
- Secure API endpoints for account and transaction management.

## Technology Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask, Python
- **Database:** SQL Server, SQLAlchemy

## Installation

### Requirements
- Python 3.8+
- Flask
- SQLAlchemy
- pytest (for running tests)

### Setup
1. Clone the repository:
   git clone https://github.com/KacperHaras/bank_distributed_database
   cd project

2. Install dependencies:
    pip install -r requirements.txt

3. Initialize your database and add initial records:
    (database/initialize.sql and database/add_records.sql)

4. Run the application:
    python run.py

### API Endpoints
- POST /account-info - Retrieves account information.
- POST /send-money - Handles money transfer between accounts.
- GET / - Serves the main login or dashboard page.

