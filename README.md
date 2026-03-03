# Ginja AI - Health Claims Validation System

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-orange.svg)

## Project Overview

**Ginja AI** is a backend service built to simulate real-time health insurance claims validation.

When a hospital submits a claim, the system performs instant checks:
- **Member eligibility** (active/inactive status)
- **Benefit limit** (maximum coverage of 40,000)
- **Fraud detection** (claim amount > 2× average procedure cost)

It returns a clear decision: **APPROVED**, **PARTIAL**, or **REJECTED**, with fraud flag and approved amount.

### The Task This Project Fulfills

The task this project fulfils is to  meet the requirements of a minimal backend service that:
- Accepts claim submissions via REST API
- Validates against eligibility, benefit limits, and simple fraud rules
- Stores claims and validation results
- Returns structured responses for downstream use for example payment permissions
- Uses clean data modeling matching the provided ERD

### ERD & Data Model

The database schema follows this Entity-Relationship Diagram:

- **Member** — patient/member info & eligibility
- **ProcedureCost** — reference table of average procedure costs
- **Claim** — main transaction (links Member + Procedure)
- **ClaimValidation** — one-to-one result with fraud flag & decision

You can view the full ERD diagram below:  
**[ERD PDF](https://docs.google.com/document/d/1GDfsKdzgKknAaZd5OOKWgeNjqbpE_08mIdt_AopC0HM/edit?usp=sharing)**

### System Architecture
You can view the system architecture diagram below:  
**[System Architecture](https://lucid.app/lucidchart/70f06ad5-b021-4553-b0f4-aeedec1865d8/edit?viewport_loc=-4628%2C-1192%2C6524%2C3344%2C0_0&invitationId=inv_95696737-c118-4011-93d1-eeb43dec1d11)**
- **Frontend Layer**: REST API (Django REST Framework + ViewSets)
- **Business Logic**: Fraud detection & validation in `fraud/services.py`
- **Data Layer**: PostgreSQL (Supabase) via Django ORM
- **Modular Design**: Three apps (`api`, `claims`, `fraud`) for clean separation
- **Documentation**: Auto-generated Swagger/OpenAPI
- **Testing**: Unit tests for models, services, and API endpoints

---

## Project Structure

```text
ginja_project/
├── api/                    
│   ├── __init__.py
│   ├── apps.py
│   ├── migrations/
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── claims/                 
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── fraud/                  
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── services.py
│   ├── tests.py
│   └── views.py
├── core/                   
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── venv/                   
├── .env                    
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
├── ginja.log
└── README.md
````
When I was building Ginja AI, I wanted the code and database to be **clean**and so i decided to build two main modules:

-(`claims` and `fraud`) and **Four tables** in the database (`Member`, `ProcedureCost`, `Claim`, `ClaimValidation`)
1. **`claims` app**  
   - This table handles the business part of the business in this case hospital submissions   
     - Who submitted it the claim
     - What medical service was done 
     - How much money is being asked for  
     - When it happened  
   - Basically: everything that describes **the claim itself**  
   - This app owns the `Member`, `ProcedureCost`, and `Claim` models
The other one is the fraud app
2. **`fraud` app**  
   - This is the smart validation part of the system
   - It does the checking of the claims submitted in the system
   - It runs the rules which include: 
     - Is the member eligible?  
     - Is the amount under the limit?  
     - Is this claim suspicious?  
   - It then creates and stores the final decision (approved, partial, rejected)  
   - This app owns the `ClaimValidation` model

I also created four tables in the ERD.
These tables are below and i'll talk about them below
1. **Member** table  
   - Purpose: store who the patient/member is  
   - I separated because a member can have many claims over time → one-to-many relationship  
   - Needed fields: ID, name, eligibility status, enrollment date

2. **ProcedureCost** table  
   - Purpose: keep a list of standard medical procedures and their **average cost**  
   - I separated because fraud rule needs to compare claim amount against average cost 
   - Needed fields: procedure code, name, average cost

3. **Claim** table  
   - Purpose: the actual claim record submitted by the hospital  
   -It  links to Member and ProcedureCost  
   - It stores the basics in  this who, what, how much, when they did the claim  
   - One claim → one validation (one-to-one with ClaimValidation)

4. **ClaimValidation** table  
   - Purpose: store the **result** of running the checks  
   - Keeps the decision separate from the claim itself  
   - I separated ir because 
     - Validation can change later like manual reviews can override  
     - Keeps claim data clean and doesnt mix everything up
     - Easy to query: "show me all rejected claims" or "count fraud flags this month"

**Why not fewer tables?**

- If I merged everything into one table → it would become huge and messy (lots of NULL fields, hard to query)
- If I didn't have a separate `ProcedureCost` → I'd have no reliable average cost for fraud checks
- If validation was inside `Claim` → harder to add new validation rules or audit history later
# How to Run Locally

## Prerequisites

- Python 3.10+
- PostgreSQL (Supabase) or local SQLite for testing
- Git

---

## Step-by-step

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd ginja_project
```

### 2. Create & activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root and add:

```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Supabase (PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
<!-- DB_PASSWORD=supabase-password -->
DB_HOST=aws-0-us-west-2.pooler.supabase.com
DB_PORT=5432
```

### 5. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

### 7. Access the API & Documentation

- **Swagger UI (interactive docs):**  
  http://127.0.0.1:8000/api/docs/

- **API root:**  
  http://127.0.0.1:8000/api/

- **Raw OpenAPI schema:**  
  http://127.0.0.1:8000/api/schema/

---

# API Endpoints (Swagger)

| Method | Endpoint | Description |
|--------|----------|------------|
| POST | `/api/claims/` | Submit a new claim |
| GET | `/api/claims/{claim_id}/` | Retrieve claim status & validation |
| GET | `/api/claims/` | List summary of all claims |

---

# Submit Claim

```bash
curl -X POST http://127.0.0.1:8000/api/claims/ \
  -H "Content-Type: application/json" \
  -d '{
    "member_id": "M_API",
    "provider_id": "H_PROVIDER",
    "diagnosis_code": "D_API",
    "procedure_code": "P_API",
    "claim_amount": 5000.00
  }'
```

---

# Get Claim Status

```bash
curl http://127.0.0.1:8000/api/claims/CABC123/
```

---

# Testing

## Run all tests

```bash
python manage.py test
```

## Specific apps

```bash
python manage.py test claims
python manage.py test fraud
python manage.py test api
```

---

# Production Improvements & Recommendations
I'd add proper authentication. Every request would require a valid token (obtained via a secure login endpoint), tied to a user or hospital account. This would let me enforce who can submit claims (only authorized providers), who can view statuses like claims officer or a member, and block unauthorized access completely. Tokens would expire automatically, support refresh tokens, and I'd add role-based permissions.

### CI/CD Pipeline – How I'd Improve It in Production

Currently there's no automated deployment process so when I get to a point of deployment and in production, I'd set up a full **CI/CD pipeline** using GitHub Actions.This way, new features, bug fixes, or fraud rule updates will go live safely.
---

# Technology Stack

- **Framework:** Django 5.2 + Django REST Framework  
- **Database:** PostgreSQL (Supabase)  
- **API Documentation:** drf-spectacular (Swagger UI)  
- **Containerization:** Docker & Docker Compose  
- **Testing:** Django Test Framework  
- **Logging:** Python logging + file handler  

---
## Features

- **Real-Time Validation**: Instantly validates claims upon submission.
- **Fraud Detection**: Implements rules to detect potentially fraudulent claims.
- **Clear Decision Outputs**: Returns straightforward results: **APPROVED**, **PARTIAL**, or **REJECTED**.
- **RESTful API**: Easy integration for front-end applications.
- **Auto-Generated Documentation**: Swagger UI for seamless API usage.
- **Unit Testing**: Comprehensive tests ensure reliability and maintainability.


