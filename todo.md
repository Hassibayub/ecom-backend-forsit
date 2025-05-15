# ✅ E-commerce Admin API - Development TODO List

This is the step-by-step checklist to implement the FastAPI-based backend for the E-commerce Admin API project.

---

## 1. �� Project Setup

- [x] Create & activate virtual environment (`.venv`)
- [x] Initialize `git` and set up `.gitignore`
- [x] Install dependencies:
  - `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `mysql-connector-python`
  - Dev/test: `pytest`, `faker`, `python-dotenv`
- [x] Set up project structure:
```
/app
/models
/schemas
/routers
/services
/db
main.py
.env
requirements.txt
seed\_data.py
```


---

## 2. ⚙️ FastAPI Boilerplate

- [x] Create `main.py` with FastAPI app instance
- [ ] Add middleware and exception handlers (optional) [no need now].
- [x] Configure environment variables with `.env`

---

## 3. 🗃️ Database Setup

- [x] Define SQLAlchemy database engine and session logic (`/db/session.py`)
- [x] Define models:
  - [x] `Product`
  - [x] `Category`
  - [x] `Sale`
  - [x] `Inventory`
- [x] Create Pydantic schemas for input/output
- [x] Run migrations manually or with Alembic (optional)

---

## 4. 🧩 Feature Implementation

### 4.1 Product Management
- [x] `POST /products`: Add new product
- [x] `GET /products`: List all products
- [x] `GET /products/{product_id}`: Product details

### 4.2 Inventory Management
- [x] `GET /inventory`: List current stock
- [x] `GET /inventory/low-stock`: Products below threshold
- [x] `PATCH /inventory/{product_id}`: Update stock

### 4.3 Sales & Revenue
- [x] `GET /sales`: Filterable sales data
- [x] `GET /sales/revenue`: Revenue by interval
- [x] `GET /sales/compare`: Revenue comparison

---

## 5. 🧪 Testing

- [x] Write unit tests for models and business logic
- [x] Write integration tests for all endpoints using FastAPI `TestClient`
- [ ] Add sample test DB or test fixtures [SKIP IT]

---

## 6. 🧰 Demo Data

- [x] Create `seed_data.py` script
- [x] Use Faker to generate:
  - [x] Sample categories
  - [x] Products with prices & stock
  - [x] Sales records with dates

---

## 7. 📘 Documentation

- [x] Generate API docs via `/docs` and `/redoc`
- [x] Write `README.md`:
  - [x] Setup instructions
  - [x] Seed script usage
  - [x] Endpoint summary
- [x] Write `database_schema.md` or include schema in README

---

## 8. 📤 Submission Prep

- [ ] Clean up codebase (linting, structure)
- [ ] Push code to public GitHub repo
- [ ] Export PRD `.md` as PDF
- [ ] Ensure all endpoints return expected data
- [ ] Add final test run logs (optional)

---

## ✅ Bonus (Optional)

- [ ] Dockerize project with `Dockerfile` + `docker-compose.yml`
- [ ] Add `.env.example`
- [ ] Add Makefile or CLI helper script
- [ ] Deploy on Render/Railway (demo link)

---