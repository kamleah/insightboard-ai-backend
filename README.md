### 🧭 **README.md** — Backend (FastAPI + Gemini AI)

# 🚀 InsightBoard AI — Backend

This is the **backend service** for the InsightBoard AI project, built using **FastAPI** and integrated with **Google Gemini Generative AI**.
It exposes RESTful APIs to process transcripts, generate actionable insights, and manage action items.

---

## 📁 Folder Structure

```
backend/
│
├── routers/                  # API version routers
│   ├── level1.py             # v1 - Transcript & Action Items (Gemini integrated)
│   └── level2.py             # v2 - Future-ready routes / Health check
│
├── .env                      # Environment variables (Gemini + frontend URL)
├── main.py                   # FastAPI entry point and app initialization
├── requirements.txt           # Python dependencies
├── README.md                  # You are here 👋
└── inVenv/                   # (optional) Local virtual environment folder
```

---

## ⚙️ Requirements

| Dependency          | Version | Purpose                |
| ------------------- | ------- | ---------------------- |
| Python              | 3.9+    | Required runtime       |
| FastAPI             | Latest  | Web framework          |
| Uvicorn             | Latest  | ASGI server            |
| python-dotenv       | Latest  | Environment management |
| google-generativeai | Latest  | Gemini API SDK         |

---

## 📦 Installation & Setup

### 1️⃣ Create Virtual Environment

```bash
cd backend
python3 -m venv inVenv
source inVenv/bin/activate   # On macOS/Linux
# OR
inVenv\Scripts\activate      # On Windows
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Configure Environment Variables

Create a `.env` file in the **backend** root with the following:

```bash
# .env
GEMINI_API_KEY=your_gemini_api_key_here
LLM_MODEL=gemini-2.5-flash
FRONTEND_URL=http://localhost:3000
```

---

## 🧠 Project Overview

### **Main Entry File:** `main.py`

Handles:

* FastAPI initialization
* CORS setup
* Gemini model configuration
* Router registration for API versioning
* Root & health check endpoints

Example snippet:

```python
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model_name = os.getenv("LLM_MODEL", "gemini-2.5-flash")
app.state.gemini_model = genai.GenerativeModel(model_name)
```

---

### **Routers**

#### 🧩 `/api/v1` → `routers/level1.py`

Implements:

* Transcript submission
* AI-powered action item extraction
* CRUD for action items

Endpoints:

| Method | Endpoint                    | Description                           |
| ------ | --------------------------- | ------------------------------------- |
| GET    | `/api/v1`                   | Root route for v1                     |
| GET    | `/api/v1/health`            | Health check                          |
| POST   | `/api/v1/transcript`        | Generate action items from transcript |
| GET    | `/api/v1/action-items`      | Fetch all action items                |
| PUT    | `/api/v1/action-items/{id}` | Update an action item                 |
| DELETE | `/api/v1/action-items/{id}` | Delete an action item                 |

---

#### 🧩 `/api/v2` → `routers/level2.py`

Implements:

* Root & Health routes for API v2
* Placeholder for future upgrades

Endpoints:

| Method | Endpoint         | Description         |
| ------ | ---------------- | ------------------- |
| GET    | `/api/v2`        | Root route for v2   |
| GET    | `/api/v2/health` | Health check for v2 |

---

## 🧪 Running the API

### Development mode:

```bash
uvicorn main:app --reload
```

Server will start at:
👉 **[http://localhost:8000](http://localhost:8000)**

---

### Health Check

Test that the API is up:

```bash
curl http://localhost:8000/health
```

Response:

```json
{
  "status": "healthy",
  "timestamp": "2025-10-30T12:34:56.789Z"
}
```

---

### Versioned Endpoints

| API Version | Root Endpoint | Example URL                                                  |
| ----------- | ------------- | ------------------------------------------------------------ |
| v1          | `/api/v1`     | [http://localhost:8000/api/v1](http://localhost:8000/api/v1) |
| v2          | `/api/v2`     | [http://localhost:8000/api/v2](http://localhost:8000/api/v2) |

---

## 🧩 Example Request

**POST** `/api/v1/transcript`

Request body:

```json
{
  "transcript": "Let's assign marketing to create campaign assets and design to prepare visuals by next Friday."
}
```

Response:

```json
{
  "actionItems": [
    {
      "id": "uuid-1",
      "text": "Marketing to create campaign assets",
      "priority": "high",
      "tags": ["@Marketing"],
      "status": "pending",
      "createdAt": "2025-10-30T10:45:00Z"
    },
    {
      "id": "uuid-2",
      "text": "Design team to prepare visuals by next Friday",
      "priority": "medium",
      "tags": ["@Design"],
      "status": "pending",
      "createdAt": "2025-10-30T10:45:00Z"
    }
  ]
}
```

---

## 🔐 CORS Configuration

Allowed Origins (in `main.py`):

```python
allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"]
```

✅ Enables your Next.js frontend to communicate with FastAPI locally.

---

## 🧩 Notes

* The project currently stores action items **in-memory** (not in a DB).
* Ideal for prototyping; for production, connect PostgreSQL or MongoDB.
* Gemini model (`gemini-2.5-flash`) is configured once and shared via `app.state`.

---

## 🧰 Requirements File Example

`requirements.txt`

```
fastapi
uvicorn
python-dotenv
google-generativeai
more...
```

---

## 🧠 Future Enhancements

* Add authentication (JWT or OAuth2)
* Integrate a database (PostgreSQL / Prisma)
* Add v2 with refined AI insights or analytics
* Dockerize backend for deployment

---

## 🔗 Related Repositories

* **Backend (FastAPI)** → [`/insightboard-ai-frontend`](https://github.com/kamleah/insightboard-ai-frontend)
* **Frontend (Next.js)** → `this folder`

---

## 👨‍💻 Contributors

| Name      | Role                 |
| --------- | -------------------- |
| Kamlesh Gupta | Full Stack Developer |
