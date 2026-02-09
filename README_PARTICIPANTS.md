# Vault Management System - Backend for Debugging Competition

This document outlines the setup, execution, and testing procedures for the Vault Management System backend, designed for a debugging competition. It includes intentionally injected bugs for participants to discover and fix.

## Project Information

- **System Topic:** Vault Management System
- **Description:** A financial institution's digital system to manage users, vaults, lockers, allocations, assets, transactions, and payments. It supports locker allocation, asset deposit/withdrawal, and access tracking with proper validation.
- **Tech Stack:**
  - Python 3.10+
  - FastAPI (Web Framework)
  - SQLAlchemy (Async ORM with `asyncpg`)
  - Pydantic (Data Validation & Schemas)
  - PostgreSQL (Database)
- **Focus:** Backend APIs only (JSON), business logic, data integrity, workflows. No frontend.
- **Architecture:** Modular backend structure as specified in the prompt.

## Setup Instructions

### Prerequisites

- Python 3.10+
- PostgreSQL database server installed and running.
- `git` (if cloning from a repository, otherwise manual file creation is assumed).

### 1. Create Project Structure and Files

Ensure your project directory matches the following structure. If you received this project as a set of files, verify the structure.

```
/project_root
├── .env
├── .gitignore
├── requirements.txt
├── alembic.ini       # DB Migrations config
└── app/
    ├── __init__.py
    ├── main.py       # App entry point
    ├── core/
    │   ├── config.py # Settings
    │   └── security.py
    ├── db/
    │   ├── session.py # Async DB engine
    │   └── base.py
    ├── models/
    │   ├── __init__.py
    │   ├── user.py
    │   ├── vault.py
    │   ├── locker.py
    │   ├── locker_allocation.py
    │   ├── asset.py
    │   ├── vault_transaction.py
    │   ├── payment.py
    │   └── access_log.py
    ├── schemas/      # Pydantic models
    │   ├── __init__.py
    │   ├── user.py
    │   ├── vault.py
    │   ├── locker.py
    │   ├── token.py
    │   ├── locker_allocation.py
    │   ├── asset.py
    │   ├── transaction.py
    │   └── payment.py
    └── api/
        ├── deps.py
        └── v1/
            ├── api.py
            └── endpoints/
                ├── auth.py
                ├── vaults.py
                ├── lockers.py
                └── transactions.py
```

### 2. Virtual Environment & Dependencies

1.  Navigate to your project root directory.
2.  Create a Python virtual environment:
    ```bash
    python -m venv .venv
    ```
3.  Activate the virtual environment:
    - On Windows:
      ```bash
      .venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```
4.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Database Setup (PostgreSQL)

1.  **Create a PostgreSQL database:**
    You'll need a PostgreSQL server running. Create a new database, for example, `vaultdb`, and a user with appropriate permissions.
    ```sql
    CREATE DATABASE vaultdb;
    CREATE USER vaultuser WITH PASSWORD 'vaultpassword';
    GRANT ALL PRIVILEGES ON DATABASE vaultdb TO vaultuser;
    ```
2.  **Configure `.env`:**
    Update the `.env` file with your database connection string and JWT secret key.
    ```
    DATABASE_URL="postgresql+asyncpg://vaultuser:vaultpassword@localhost/vaultdb"
    SECRET_KEY="your_super_secret_key" # IMPORTANT: Change this to a strong, random string
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```
    Replace `vaultuser`, `vaultpassword`, `localhost`, and `vaultdb` with your actual database credentials and host if they differ. Change `SECRET_KEY` to a unique, strong key.

### 4. Database Migrations (Alembic)

1.  **Initialize Alembic:**
    ```bash
    alembic init alembic
    ```
    _NOTE:_ If `alembic` directory already exists, skip this step.
2.  **Update `alembic.ini`:**
    In alembic/ created, The `env.py` generated must contain the below code to initialize our project properly.

    Note: alembic uses psyopg2 and not asyncpg
    `sqlalchemy.url = postgresql+psycopg2://vaultuser:vaultpassword@localhost/vaultdb`

    In `alembic/env.py`, ensure `target_metadata` is set correctly to import your `Base` from `app.db.base` and all your models.

    Find the line `from app.db.base import Base` and make sure `target_metadata = Base.metadata`. You might need to add `import app.models` to ensure all models are registered with the metadata.

    ```python
    # alembic/env.py excerpt
    import sys
    import os
    sys.path.append(os.getcwd())

    from logging.config import fileConfig

    from sqlalchemy import engine_from_config
    from sqlalchemy import pool

    from alembic import context
    from app.core.config import settings

    # this is the Alembic Config object, which provides
    # access to values within the .ini file in use.
    config = context.config

    # Load the database url from settings and optimize it for sqlalchemy
    # Set the url to alembic environment securely
    db_url = settings.DATABASE_URL.replace("asyncpg","psycopg2")
    config.set_main_option("sqlalchemy.url", db_url)

    # Interpret the config file for Python logging.
    # This line sets up loggers basically.
    if config.config_file_name is not None:
        fileConfig(config.config_file_name)

    # add your model's Base object here
    # for 'autogenerate' support
    # from myapp import mymodel
    from app.db.base import Base
    import app.models # <--- IMPORTANT: Import your models to ensure Base.metadata is populated
    target_metadata = Base.metadata

    # ... rest of the file ...
    ```

3.  **Generate initial migration script:**
    ```bash
    alembic revision --autogenerate -m "Initial migration"
    ```
4.  **Apply migrations to the database:**
    ```bash
    alembic upgrade head
    ```

## Running the Application

To start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The application will be accessible at `http://127.0.0.1:8000`.

## Accessing API Endpoints

Once the server is running, you can access the interactive API documentation (Swagger UI) at:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Or ReDoc at:
[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Use these interfaces to interact with the API endpoints.

## User Flow for Testing & Debugging (Linear Walkthrough)

This flow guides you through typical interactions and helps in uncovering the injected bugs.

---

### **Phase 1: Admin Operations**

1.  **Register Admin User**
    - **Endpoint:** `POST /api/v1/auth/register`
    - **Body:**
      ```json
      {
        "email": "admin@example.com",
        "password": "adminpassword",
        "name": "Admin",
        "phone": "1234567890",
        "role": "ADMIN",
        "status": "ACTIVE"
      }
      ```
    - **Expected:** Successful user creation.
2.  **Login as Admin**
    - **Endpoint:** `POST /api/v1/auth/login`
    - **Form Data (x-www-form-urlencoded):**
      - `username`: `Admin`
      - `password`: `adminpassword`
    - **Expected:** `access_token`. Copy this token; you'll need it for authenticated requests.
3.  **Create a Vault**
    - **Endpoint:** `POST /api/v1/vaults/create`
    - **Headers:** `Authorization: Bearer <ADMIN_ACCESS_TOKEN>`
    - **Body:**
      ```json
      {
        "location": "Downtown Branch",
        "total_lockers": 100,
        "available_lockers": 100,
        "status": "OPERATIONAL"
      }
      ```
    - **Expected:** Successful vault creation with assigned ID. Note the `id` of the created vault.
4.  **List all Vaults**
    - **Endpoint:** `GET /api/v1/vaults/list`
    - **Headers:** `Authorization: Bearer <ADMIN_ACCESS_TOKEN>`
    - **Body:**
      ```json
      {
        "location": "Downtown Branch",
        "total_lockers": 100,
        "available_lockers": 100,
        "status": "OPERATIONAL"
      }
      ```
    - **Expected:** On success, Responds with all the vault `id`
5.  **Create Lockers within the Vault**
    - **Endpoint:** `POST /api/v1/lockers/vaults/{vault_id}/` (replace `{vault_id}` with any value form /list endpoint)
    - **Headers:** `Authorization: Bearer <ADMIN_ACCESS_TOKEN>`
    - **Body:**
      ```json
      {
        "vault_id": 1,
        "locker_number": "A001",
        "size": "SMALL",
        "monthly_rent": 50.0,
        "status": "AVAILABLE"
      }
      ```
      Create a few more, e.g., "A002", "B001" with different sizes/rents.
    - **Expected:** Successful locker creation. Note the `id` of at least one locker.

---

### **Phase 2: Customer Operations**

1.  **Register Customer User**
    - **Endpoint:** `POST /api/v1/auth/register`
    - **Body:**
      ```json
      {
        "email": "customer@example.com",
        "password": "customerpassword",
        "name": "Customer",
        "phone": "0987654321",
        "role": "CUSTOMER",
        "status": "ACTIVE"
      }
      ```
    - **Expected:** Successful user creation.
2.  **Login as Customer**
    - **Endpoint:** `POST /api/v1/auth/login`
    - **Form Data (x-www-form-urlencoded):**
      - `username`: `Customer`
      - `password`: `customerpassword`
    - **Expected:** `access_token`. Copy this token.
3.  **Check Available Lockers**
    - **Endpoint:** `GET /api/v1/lockers/available`
    - **Headers:** `Authorization: Bearer <CUSTOMER_ACCESS_TOKEN>`
    - **Parameters:** Optionally filter by `size` or `vault_id`.
    - **Expected:** List of available lockers.
4.  **Allocate a Locker**
    - **Endpoint:** `POST /api/v1/lockers/{locker_id}/allocate` (replace `{locker_id}` with an available locker id)
    - **Headers:** `Authorization: Bearer <CUSTOMER_ACCESS_TOKEN>`
    - **Parameters:** `expiry_date` (optional, defaults to 30 days from now)
    - **Expected:** Successful allocation with allocation ID.
5.  **Customer Transactions Operations**
    - **Add Asset to Locker:**
      - **Endpoint:** `POST /api/v1/transactions/allocations/{allocation_id}/assets`
      - **Headers:** `Authorization: Bearer <CUSTOMER_ACCESS_TOKEN>`
      - **Body:**
        ```json
        {
          "asset_name": "Gold Watch",
          "estimated_value": 5000.0,
          "type": "JEWELRY"
        }
        ```
      - **Expected:** Asset added successfully with transaction log.
    - **Pay Rent for Allocation:**
      - **Endpoint:** `POST /api/v1/transactions/allocations/{allocation_id}/pay_rent`
      - **Headers:** `Authorization: Bearer <CUSTOMER_ACCESS_TOKEN>`
      - **Body:**
        ```json
        {
          "amount": 50.0
        }
        ```
      - **Expected:** Payment processed successfully and expiry date extended by 30 days.
    - **Remove Asset from Locker:**
      - **Endpoint:** `DELETE /api/v1/transactions/assets/{asset_id}`
      - **Headers:** `Authorization: Bearer <CUSTOMER_ACCESS_TOKEN>`
      - **Expected:** Asset removed successfully with withdrawal transaction log.

---

### **Phase 3: Debugging Scenarios (Focus on discovering bugs)**

The system contains total of 5 bugs, Your job is to test the endpoints following the above user flow and identify bugs. Make sure the endpoints behave properly as stated in this section

## ❌ What is Broken?

- Vault availability counts become inconsistent after allocations.
- Invalid or negative payments sometimes get processed.
- Assets can be accessed even after allocation expiry.
- Locker allocation APIs occasionally crash.
- Concurrent allocation requests cause inconsistent states.
- Access operations sometimes bypass validation checks.

---

## ✅ Definition of Done

- Proper ACID transactions and available values all the time.
- Lockers can only be allocated when available and valid.
- Vault and locker counts always remain consistent.
- Payments accept only valid positive amounts.
- Expired allocations cannot perform locker operations.
- Asset operations respect allocation status.
- Only authorized users can perform operations.
- System remains stable under concurrent requests.

---

Good luck debugging!
