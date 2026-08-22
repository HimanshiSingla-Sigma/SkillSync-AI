# 🚀 CareerConnect AI — Autonomous Placement & Knowledge Graph Platform

**CareerConnect AI** is an intelligent university placement and recruitment automation platform combining **Dual-Database Architecture (MongoDB Atlas + Neo4j Aura Graph Database)**, **Rule-Based Deterministic Eligibility Policies**, **Automated Resume Parsing**, and **Graph-Augmented Retrieval-Augmented Generation (GraphRAG)**.

---

## ⚡ Quickstart Guide (Run in 1 Minute)

### 1. Requirements
- Python 3.10+ (Python 3.11 / 3.12 / 3.13 supported)
- Internet connection (Databases are pre-connected in the cloud)

### 2. Setup & Installation

```bash
# 1. Open terminal in the project directory
cd SkillSyncAi

# 2. Create and activate a virtual environment
# On macOS / Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows (PowerShell / Command Prompt):
python -m venv venv
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### 3. Start the Platform

```bash
# Run the unified full-stack server:
uvicorn app.main:app --reload --port 8000
```

### 4. Open in Your Browser
👉 Open **[http://localhost:8000](http://localhost:8000)** in your browser!

> ⚠️ **Note:** The entire modern animated platform runs directly on **`http://localhost:8000`** (served by FastAPI). You **do not** need to run `npm` or `node`.

---

## 🌟 Key Platform Features

1. **Deterministic Eligibility Engine**:
   - Zero hallucination policy gate checking candidate CGPA, active backlogs, enrolled programme, and mandatory skills.
2. **Interactive Neo4j Knowledge Graph Canvas**:
   - Live visualizer rendering multi-hop relationships: `(Student)-[:HAS_SKILL]->(Skill)<-[:REQUIRES]-(PlacementDrive)`.
3. **GraphRAG AI Career Agent**:
   - Multi-intent AI reasoning agent answering queries on live drive eligibility, skill gaps, roadmaps, and compensation packages.
4. **Real Gmail SMTP Verification**:
   - Secure transactional email dispatch sending magic activation links and 6-digit OTP codes directly to candidate Gmail inboxes.
5. **Resume Studio & Profile Matrix**:
   - Automated skill extraction syncing candidate profiles directly to MongoDB Atlas and Neo4j Aura in real time.

---

## ⚙️ Environment Configuration (`.env`)

Copy `.env.example` to `.env` if you wish to customize credentials:

```ini
# MongoDB Atlas
MONGODB_URI="mongodb+srv://..."
MONGODB_DB_NAME="careerconnect_ai"

# Neo4j Aura Graph Database
NEO4J_URI="neo4j+s://..."
NEO4J_USERNAME="..."
NEO4J_PASSWORD="..."

# Gmail SMTP Authentication (For Real Email Verification)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="your-email@gmail.com"
SMTP_PASSWORD="your-16-character-app-password"
EMAILS_FROM_EMAIL="your-email@gmail.com"
FRONTEND_URL="http://localhost:8000"
```

---

## 🏛️ System Architecture

```
                       ┌────────────────────────┐
                       │   FastAPI Full-Stack   │
                       │ (http://localhost:8000)│
                       └───────────┬────────────┘
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         │                                                   │
         ▼                                                   ▼
┌──────────────────┐                               ┌───────────────────┐
│  MongoDB Atlas   │                               │    Neo4j Aura     │
│ (Primary Store)  │                               │ (Knowledge Graph) │
│ - Students       │                               │ - Student Nodes   │
│ - Companies      │                               │ - Skill Nodes     │
│ - Drives         │                               │ - Drive Nodes     │
│ - Applications   │                               │ - Multi-Hop Graph │
└──────────────────┘                               └───────────────────┘
```

---

## 🧪 Testing

To run the automated test suite:

```bash
pytest
```