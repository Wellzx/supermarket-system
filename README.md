# Supermarket System

A terminal-based supermarket management system built with Python and PostgreSQL.

## Technologies

- Python 3.10+
- PostgreSQL 18
- psycopg3
- python-dotenv

## Features

- Categories management
- Suppliers management
- Roles management
- Products management (linked to categories and suppliers)
- Customers management
- Employees management (linked to roles)
- Sales management (with automatic stock control)

## Project Structure

supermarket/
├── .env
├── .gitignore
├── requirements.txt
├── schema.sql
├── main.py
└── modules/
    ├── __init__.py
    ├── database.py
    ├── categories.py
    ├── suppliers.py
    ├── roles.py
    ├── products.py
    ├── customers.py
    ├── employees.py
    └── sales.py

## Setup

### 1. Clone the repository
git clone https://github.com/Wellzx/supermarket-system.git
cd supermarket-system

### 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Configure environment variables
Create a .env file in the root directory:

DB_HOST=localhost
DB_NAME=supermarket
DB_USER=your_user
DB_PASSWORD=your_password
DB_PORT=5432

### 5. Create the database
psql -U your_user -h localhost -c "CREATE DATABASE supermarket;"

### 6. Create the tables
psql -U your_user -d supermarket -h localhost -f schema.sql

### 7. Run the project
python main.py

## Future improvements
- Allow partial updates (update only the fields you want to change)
- Add authentication and user roles
- Generate sales reports
- REST API with FastAPI
