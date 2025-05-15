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

- [ ] Create `main.py` with FastAPI app instance
- [ ] Add middleware and exception handlers (optional)
- [ ] Configure environment variables with `.env`

---

## 3. 🗃️ Database Setup

- [ ] Define SQLAlchemy database engine and session logic (`/db/session.py`)
- [ ] Define models:
  - [ ] `Product`
  - [ ] `Category`
  - [ ] `Sale`
  - [ ] `Inventory`
- [ ] Create Pydantic schemas for input/output
- [ ] Run migrations manually or with Alembic (optional)

---

## 4. 🧩 Feature Implementation

### 4.1 Product Management
- [ ] `POST /products`: Add new product
- [ ] `GET /products`: List all products
- [ ] `GET /products/{product_id}`: Product details

### 4.2 Inventory Management
- [ ] `GET /inventory`: List current stock
- [ ] `GET /inventory/low-stock`: Products below threshold
- [ ] `PATCH /inventory/{product_id}`: Update stock

### 4.3 Sales & Revenue
- [ ] `GET /sales`: Filterable sales data
- [ ] `GET /sales/revenue`: Revenue by interval
- [ ] `GET /sales/compare`: Revenue comparison

---

## 5. 🧪 Testing

- [ ] Write unit tests for models and business logic
- [ ] Write integration tests for all endpoints using FastAPI `TestClient`
- [ ] Add sample test DB or test fixtures

---

## 6. 🧰 Demo Data

- [ ] Create `seed_data.py` script
- [ ] Use Faker to generate:
  - [ ] Sample categories
  - [ ] Products with prices & stock
  - [ ] Sales records with dates

---

## 7. 📘 Documentation

- [ ] Generate API docs via `/docs` and `/redoc`
- [ ] Write `README.md`:
  - [ ] Setup instructions
  - [ ] Seed script usage
  - [ ] Endpoint summary
- [ ] Write `database_schema.md` or include schema in README

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