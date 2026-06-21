# Chapter 7: System Design and Architecture

## 7.1 Introduction

The system design of the Smart Medical Assistant encompasses the complete architectural specification of the software system, including component decomposition, interaction patterns, data flows, API contracts, and technology stack selection. This chapter presents a comprehensive, implementation-oriented design document that serves as the blueprint for development, deployment, and maintenance of the system. The design emphasizes modularity, scalability, and separation of concerns, ensuring that each subsystem can be developed, tested, and deployed independently.

The Smart Medical Assistant follows a modern web application architecture with a clear separation between the frontend presentation layer, the backend API layer, and the data persistence layer. This three-tier architecture is a well-established pattern for web applications, providing flexibility in technology selection, ease of deployment, and straightforward horizontal scaling as user demand grows.

## 7.2 System Architecture Diagram

The following Mermaid diagram represents the high-level system architecture:

```mermaid
graph TB
    subgraph "Client Layer"
        UI[Web Browser<br/>HTML/CSS/JS]
        Mobile[Mobile Browser<br/>Responsive Design]
    end

    subgraph "Application Layer"
        Flask[Flask Web Server<br/>Port 5000]
        
        subgraph "API Endpoints"
            API1[/api/analyze]
            API2[/api/predict]
            API3[/api/diseases]
            API4[/api/symptoms]
            API5[/api/health]
        end
        
        subgraph "Core Services"
            NLP[Symptom NLP Extractor]
            ML[Disease Predictor<br/>XGBoost Model]
            Auth[Authentication Service]
            Logger[Audit Logger]
        end
        
        CORS[CORS Middleware]
    end

    subgraph "Data Layer"
        MySQL[(MySQL Database<br/>Disease Info<br/>User Data<br/>Predictions)]
        ModelFile[Model Files<br/>xgb_pipeline.pkl<br/>tfidf_vectorizer.pkl]
        SymptomDict[Symptom Dictionary<br/>JSON Config]
    end

    UI -->|HTTP GET/POST| CORS
    Mobile -->|HTTP GET/POST| CORS
    CORS --> Flask
    Flask --> API1 & API2 & API3 & API4 & API5
    API1 --> NLP
    API2 --> ML
    API3 --> MySQL
    API4 --> MySQL
    API5 --> Flask
    NLP --> ML
    ML --> ModelFile
    NLP --> SymptomDict
    Auth --> MySQL
    Logger --> MySQL
    Flask --> Auth
    Flask --> Logger
```

### 7.2.1 ASCII Architecture Representation

For environments where Mermaid rendering is unavailable, the following ASCII diagram provides an equivalent representation:

```
+--------------------------------------------------------------------------+
|                           CLIENT LAYER                                    |
|  +------------------+        +-----------------------------------+      |
|  |  Web Browser     |        |  Mobile Browser (Responsive)      |      |
|  |  HTML/CSS/JS     |        |  HTML/CSS/JS                      |      |
|  +--------+---------+        +------------------+--------+-------+      |
|           |                                     |                        |
|           | HTTP GET/POST                       | HTTP GET/POST          |
|           |                                     |                        |
+-----------|-------------------------------------|------------------------+
            |                                     |
+-----------|-------------------------------------|------------------------+
|           v                                     v                        |
|  +--------+---------+    +------------------+  +--------+-------+       |
|  |  CORS Middleware |    |  CORS Middleware |  |                |        |
|  |  (Cross-Origin)  |    |  (Cross-Origin)  |  |                |        |
|  +--------+---------+    +--------+---------+  |                |        |
|           |                       |             |                |        |
|           +-----------+-----------+             |                |        |
|                       v                         |                |        |
|           +---------------------------+         |                |        |
|           |    FLASK WEB SERVER       |         |                |        |
|           |    Port 5000              |         |                |        |
|           |    Python 3.9+            |         |                |        |
|           +-----------+---------------+         |                |        |
|                       |                         |                |        |
|           +-----------+-----------+             |                |        |
|           |                       |             |                |        |
|           v                       v             |                |        |
|  +----------------+  +------------------+       |                |        |
|  | API Endpoints  |  | Core Services    |       |                |        |
|  |                |  |                  |       |                |        |
|  | /api/analyze   |  | +-------------+ |       |                |        |
|  | /api/predict   |  | | NLP Engine  | |       |                |        |
|  | /api/diseases  |  | +-------------+ |       |                |        |
|  | /api/symptoms  |  | +-------------+ |       |                |        |
|  | /api/health    |  | | ML Predictor| |       |                |        |
|  |                |  | +-------------+ |       |                |        |
|  +----------------+  | +-------------+ |       |                |        |
|                      | | Auth Service| |       |                |        |
|                      | +-------------+ |       |                |        |
|                      | +-------------+ |       |                |        |
|                      | | Audit Logger| |       |                |        |
|                      | +-------------+ |       |                |        |
|                      +------------------+       |                |        |
|                               |                 |                |        |
|           +-------------------+-----------------+                |        |
|           |                   |                                  |        |
|           v                   v                                  |        |
|  +----------------+  +--------------------+                     |        |
|  | DATA LAYER     |  | MODEL ASSETS       |                     |        |
|  |                |  |                    |                     |        |
|  | +-----------+  |  | xgb_pipeline.pkl   |                     |        |
|  | | MySQL DB  |  |  | tfidf_vectorizer   |                     |        |
|  | | (Disease  |  |  | label_encoder.pkl  |                     |        |
|  | |  Users,   |  |  | symptom_dict.json  |                     |        |
|  | |  Predict, |  |  |                    |                     |        |
|  | |  Advice)  |  |  +--------------------+                     |        |
|  | +-----------+  |                                                |        |
|  +----------------+                                                |        |
+--------------------------------------------------------------------------+
```

## 7.3 Component Interaction

The Smart Medical Assistant is composed of six primary components that interact through well-defined interfaces. Each component has a single, clearly scoped responsibility, following the Single Responsibility Principle.

### 7.3.1 Component Definitions

| Component | Technology | Responsibility | Interface |
|-----------|------------|----------------|-----------|
| **Web Client** | HTML5, CSS3, JavaScript | User interface, symptom input, results display | REST API over HTTP |
| **Flask API Server** | Python 3.9, Flask 2.x | HTTP request handling, routing, middleware | WSGI / HTTP |
| **NLP Engine** | Python, NLTK, regex | Symptom extraction from natural language | Python function call |
| **ML Predictor** | Python, scikit-learn, XGBoost | Disease classification from structured symptoms | Python function call |
| **Authentication Service** | Python, Flask, Werkzeug | User registration, login, session management | Python function call / Database |
| **Data Persistence** | MySQL 8.0 | Structured data storage, query processing | SQL / SQLAlchemy |

### 7.3.2 Component Interaction Diagram

The following sequence describes the typical interaction flow for a symptom analysis request:

```
User                    Web Client              Flask API           NLP Engine          ML Predictor          MySQL
 |                          |                       |                   |                     |              |
 |--"I have headache..."--> |                       |                   |                     |              |
 |                          |--POST /api/analyze--> |                   |                     |              |
 |                          |                       |--extract_symptoms->|                     |              |
 |                          |                       |                   |--[extracted_symptoms]|              |
 |                          |                       |<--symptoms_list---|                     |              |
 |                          |                       |--predict_disease->|                     |              |
 |                          |                       |                   |                     |--[predict]   |
 |                          |                       |                   |<--disease_probs-------|              |
 |                          |                       |--fetch_details--->|                     |--[SQL Query]  |
 |                          |                       |                   |                     |              |
 |                          |                       |<--disease_info----|                     |<--results-----|
 |                          |<--JSON Response------|                   |                     |              |
 |<--Display Results--------|                       |                   |                     |              |
```

## 7.4 Data Flow

The data flow through the system follows a pipeline pattern, with data transforming at each stage from unstructured user input to structured prediction output. The flow is unidirectional for the prediction path, with a separate feedback path for user history and audit logging.

### 7.4.1 Primary Data Flow: Symptom Analysis

```
Stage 1: User Input Collection
+-------------------------------------------------------------------+
| Input: Raw text string (e.g., "I have severe headache and fever") |
| Origin: Web browser form submission                               |
| Transport: HTTP POST request with JSON payload                    |
| Format: { "description": "I have severe headache and fever" }       |
+-------------------------------------------------------------------+
                              |
                              v
Stage 2: API Request Processing
+-------------------------------------------------------------------+
| Input: HTTP POST to /api/analyze                                  |
| Processing: Flask parses JSON, validates input, applies CORS      |
| Output: Validated request dictionary                              |
+-------------------------------------------------------------------+
                              |
                              v
Stage 3: NLP Symptom Extraction
+-------------------------------------------------------------------+
| Input: User description string                                    |
| Processing: Tokenization, normalization, pattern matching,        |
|             negation detection, severity/duration extraction        |
| Output: Structured symptom list with metadata                     |
| Format: [{canonical_name, confidence, severity, negated, ...}]    |
+-------------------------------------------------------------------+
                              |
                              v
Stage 4: Feature Vector Construction
+-------------------------------------------------------------------+
| Input: Structured symptom list                                    |
| Processing: Canonical symptom names joined → TF-IDF vectorization |
| Output: Sparse feature vector (1 × 312)                           |
+-------------------------------------------------------------------+
                              |
                              v
Stage 5: ML Disease Prediction
+-------------------------------------------------------------------+
| Input: TF-IDF feature vector                                      |
| Processing: XGBoost predict_proba → disease probability scores    |
| Output: Disease probability distribution (30 classes)             |
+-------------------------------------------------------------------+
                              |
                              v
Stage 6: Disease Information Enrichment
+-------------------------------------------------------------------+
| Input: Top predicted disease IDs                                  |
| Processing: MySQL query for disease details, treatment,           |
|             precautions, and severity classification                |
| Output: Complete disease information records                      |
+-------------------------------------------------------------------+
                              |
                              v
Stage 7: Response Assembly and Logging
+-------------------------------------------------------------------+
| Input: Disease predictions + disease details + extraction metadata  |
| Processing: JSON serialization, confidence formatting,            |
|             audit log entry creation                              |
| Output: HTTP JSON response                                        |
+-------------------------------------------------------------------+
                              |
                              v
Stage 8: Client-Side Presentation
+-------------------------------------------------------------------+
| Input: JSON response with predictions and recommendations         |
| Processing: DOM manipulation, card rendering, chart display       |
| Output: Rendered HTML with disease prediction cards               |
+-------------------------------------------------------------------+
```

### 7.4.2 Secondary Data Flow: User Registration and Authentication

```
User            Web Client         Flask API         Auth Service       MySQL
 |                  |                   |                   |              |
 |--"Register..."--> |                   |                   |              |
 |                  |--POST /api/register->|                  |              |
 |                  |                   |--validate_input->|              |
 |                  |                   |                   |              |
 |                  |                   |--hash_password-> |              |
 |                  |                   |                   |              |
 |                  |                   |<--password_hash--|              |
 |                  |                   |--insert_user---->|              |
 |                  |                   |                   |--[INSERT]     |
 |                  |                   |                   |              |
 |                  |                   |<--user_id---------|              |
 |                  |<--success_response--|                |              |
 |<--Confirmation---|                   |                   |              |
```

### 7.4.3 Data Flow Diagram (ASCII)

```
+-------------+     +------------+     +-------------+     +--------------+
|   USER      |     |   FLASK    |     |    NLP      |     |     ML       |
|  BROWSER    |---->|   API      |---->|  ENGINE     |---->|  PREDICTOR   |
+-------------+     +------------+     +-------------+     +--------------+
       |                   |                   |                   |
       |                   |                   |                   |
       |                   |                   |                   |
       |                   v                   |                   |
       |            +-------------+            |                   |
       |            |   MySQL     |            |                   |
       |            |  DATABASE   |<-----------|-------------------|
       |            +-------------+            |                   |
       |                   |                   |                   |
       |                   |                   |                   |
       |<------------------|                   |                   |
       |    JSON Response  |                   |                   |
       |                   |                   |                   |
+-------------+     +------------+     +-------------+     +--------------+
|   USER      |     |   FLASK    |     |    NLP      |     |     ML       |
|  BROWSER    |<----|   API      |<----|  ENGINE     |<----|  PREDICTOR   |
+-------------+     +------------+     +-------------+     +--------------+
       |
       | (Render Results)
       v
+-------------+
|  DISPLAYED  |
|  PREDICTION |
+-------------+
```

## 7.5 Technology Stack

The technology stack for the Smart Medical Assistant is selected based on criteria including development productivity, library ecosystem maturity, deployment simplicity, and team expertise. The stack is deliberately conservative, favoring well-established technologies over bleeding-edge frameworks to ensure stability and maintainability.

### 7.5.1 Backend Stack

| Layer | Technology | Version | Purpose | Rationale |
|-------|-----------|---------|---------|-----------|
| **Language** | Python | 3.9+ | Primary development language | Rich ML ecosystem, readable syntax, extensive libraries |
| **Web Framework** | Flask | 2.3.x | HTTP API server | Lightweight, flexible, excellent for REST APIs |
| **WSGI Server** | Werkzeug | 2.3.x | Development server / WSGI utilities | Bundled with Flask, reliable for development |
| **Production Server** | Gunicorn | 21.x | Production WSGI server | Multi-worker process model, robust, widely used |
| **ML Framework** | scikit-learn | 1.3.x | ML utilities, preprocessing, metrics | Industry standard for classical ML |
| **Boosting Library** | XGBoost | 1.7.x | Gradient boosting classifier | Best-in-class performance, Python API |
| **NLP Library** | NLTK | 3.8.x | Text processing, tokenization, lemmatization | Mature, well-documented, adequate for symptom extraction |
| **Database ORM** | SQLAlchemy | 2.0.x | Database abstraction, query building | SQL-agnostic, powerful ORM, widely adopted |
| **Database Driver** | PyMySQL | 1.1.x | MySQL connectivity from Python | Pure Python, no external dependencies |
| **Data Processing** | pandas | 2.0.x | Data manipulation, analysis | De facto standard for tabular data in Python |
| **Numerical Computing** | NumPy | 1.24.x | Array operations, numerical computing | Foundation of scientific Python ecosystem |
| **Serialization** | joblib | 1.3.x | Model serialization and deserialization | Efficient for scikit-learn objects |
| **Authentication** | Werkzeug Security | 2.3.x | Password hashing, session management | Built-in, battle-tested security utilities |

### 7.5.2 Frontend Stack

| Layer | Technology | Version | Purpose | Rationale |
|-------|-----------|---------|---------|-----------|
| **Markup** | HTML5 | — | Page structure | Semantic, accessible, universally supported |
| **Styling** | CSS3 | — | Visual presentation | Modern selectors, flexbox/grid layouts, animations |
| **Interactivity** | JavaScript | ES6+ | Dynamic behavior, API calls | Native browser support, no build step required |
| **HTTP Client** | Fetch API | Native | AJAX requests to backend | Modern, promise-based, no external library needed |
| **Charts** | Chart.js | 4.x | Data visualization (if applicable) | Lightweight, canvas-based, easy integration |
| **Icons** | Font Awesome | 6.x | UI icons | Comprehensive icon library, CDN delivery |
| **Fonts** | Google Fonts | — | Typography (Inter, Roboto) | Free, CDN-hosted, excellent readability |

### 7.5.3 Data Layer Stack

| Technology | Version | Purpose | Rationale |
|-----------|---------|---------|-----------|
| **MySQL** | 8.0 | Relational database | ACID compliance, excellent performance, free and open-source |
| **InnoDB** | Built-in | Storage engine | Transaction support, foreign key constraints, row-level locking |
| **JSON** | Native (MySQL 8.0) | Semi-structured data storage | Native JSON functions for flexible schema extensions |

### 7.5.4 Infrastructure and Deployment Stack

| Technology | Version | Purpose | Rationale |
|-----------|---------|---------|-----------|
| **Operating System** | Ubuntu 22.04 LTS | Server OS | Stable, long-term support, excellent Python ecosystem |
| **Reverse Proxy** | Nginx | 1.24 | HTTP reverse proxy, static file serving, SSL termination | High performance, proven reliability, extensive configuration options |
| **Process Manager** | systemd | Built-in | Service management, auto-restart, logging | Standard on Ubuntu, no additional dependencies |
| **SSL/TLS** | Let's Encrypt | — | HTTPS certificate provisioning | Free, automated, widely trusted |
| **Containerization** | Docker | 24.x | Application packaging, environment consistency | Portable, reproducible deployments |
| **Version Control** | Git | 2.x | Source code management | Industry standard, distributed |

### 7.5.5 Development and Testing Tools

| Tool | Purpose | Rationale |
|------|---------|-----------|
| **pytest** | Unit and integration testing | Powerful, extensible, excellent fixture support |
| **pytest-flask** | Flask-specific testing utilities | Seamless integration with Flask app context |
| **coverage.py** | Code coverage analysis | Identifies untested code paths |
| **flake8** | Code linting and style checking | Enforces PEP 8 compliance, catches syntax errors |
| **black** | Code formatting | Automatic, deterministic formatting eliminates style debates |
| **Postman / curl** | API testing | Manual and automated REST API validation |
| **VS Code** | Integrated development environment | Python extensions, debugging, Git integration |

## 7.6 API Design

The Flask backend exposes a RESTful API with five primary endpoints, designed around resource-oriented principles and consistent JSON request/response formats. All endpoints support Cross-Origin Resource Sharing (CORS) to enable frontend applications hosted on different domains to interact with the API.

### 7.6.1 API Specification Overview

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/health` | GET | Health check and system status | None |
| `/api/symptoms` | GET | Retrieve list of supported symptoms | None |
| `/api/diseases` | GET | Retrieve list of diseases with details | None |
| `/api/analyze` | POST | Analyze symptom description and return predictions | Optional |
| `/api/predict` | POST | Predict disease from structured symptom list | Optional |

### 7.6.2 CORS Configuration

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all domains (development)
# In production, restrict to specific origins
cors = CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:8080", "https://yourdomain.com"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
    }
})
```

### 7.6.3 Endpoint: `/api/health`

**Purpose:** System health check and availability verification.

**Request:**
```bash
GET /api/health
Content-Type: application/json
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2024-06-15T14:30:00Z",
  "version": "1.0.0",
  "services": {
    "api": "up",
    "database": "up",
    "model": "up"
  },
  "model_info": {
    "name": "XGBoost Medical Classifier",
    "accuracy": 0.9632,
    "classes": 30,
    "features": 312
  }
}
```

**Response (503 Service Unavailable):**
```json
{
  "status": "degraded",
  "timestamp": "2024-06-15T14:30:00Z",
  "services": {
    "api": "up",
    "database": "down",
    "model": "up"
  },
  "error": "Database connection failed"
}
```

### 7.6.4 Endpoint: `/api/symptoms`

**Purpose:** Retrieve the complete list of symptoms supported by the system, including canonical names and category information.

**Request:**
```bash
GET /api/symptoms
Content-Type: application/json
```

**Response (200 OK):**
```json
{
  "count": 62,
  "symptoms": [
    {
      "id": "fever",
      "name": "Fever",
      "category": "general",
      "description": "Elevated body temperature above normal range",
      "common_diseases": ["Common Cold", "Pneumonia", "Malaria", "Typhoid"]
    },
    {
      "id": "chest_pain",
      "name": "Chest Pain",
      "category": "cardiovascular",
      "description": "Pain or discomfort in the chest area",
      "common_diseases": ["Heart Attack", "Hypertension", "GERD", "Asthma"]
    },
    {
      "id": "headache",
      "name": "Headache",
      "category": "neurological",
      "description": "Pain in the head or upper neck region",
      "common_diseases": ["Migraine", "Hypertension", "Common Cold", "Allergy"]
    }
    // ... additional symptoms
  ]
}
```

### 7.6.5 Endpoint: `/api/diseases`

**Purpose:** Retrieve comprehensive information about all diseases in the system database, including descriptions, treatments, and precautions.

**Request:**
```bash
GET /api/diseases
Content-Type: application/json
```

**Query Parameters:**
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `severity` | string | Filter by severity level (mild, moderate, severe) | None |
| `limit` | integer | Maximum number of results to return | 100 |
| `offset` | integer | Number of results to skip | 0 |

**Response (200 OK):**
```json
{
  "count": 30,
  "diseases": [
    {
      "id": 1,
      "name": "Fungal Infection",
      "severity": "Mild",
      "description": "A fungal infection is a skin disease caused by fungi...",
      "common_symptoms": ["itching", "skin_rash", "nodal_skin_eruptions", "dischromic_patches"],
      "treatment": "Consult a dermatologist. Maintain hygiene. Use antifungal creams...",
      "precautions": ["bath twice", "use detol or neem in bathing water", "keep infected area dry", "use clean cloths"]
    },
    {
      "id": 2,
      "name": "Allergy",
      "severity": "Mild",
      "description": "An allergy is an immune system response to a foreign substance...",
      "common_symptoms": ["continuous_sneezing", "shivering", "chills", "watering_from_eyes"],
      "treatment": "Avoid allergens. Take antihistamines. Consult an allergist...",
      "precautions": ["avoid allergen exposure", "use protective gear", "keep surroundings clean", "consult doctor"]
    }
    // ... additional diseases
  ]
}
```

### 7.6.6 Endpoint: `/api/analyze` (Primary)

**Purpose:** Accept a natural language symptom description, extract structured symptoms, predict the most likely diseases, and return comprehensive results with treatment recommendations and precautions.

**Request:**
```bash
POST /api/analyze
Content-Type: application/json

{
  "description": "I have severe headache and mild fever for 3 days, with some chest pain",
  "user_id": "optional_user_id",
  "return_top_k": 3
}
```

**Request Body Schema:**
```json
{
  "description": {
    "type": "string",
    "required": true,
    "minLength": 10,
    "maxLength": 1000,
    "description": "Natural language symptom description"
  },
  "user_id": {
    "type": "string",
    "required": false,
    "description": "Optional user identifier for history tracking"
  },
  "return_top_k": {
    "type": "integer",
    "required": false,
    "default": 3,
    "minimum": 1,
    "maximum": 5,
    "description": "Number of top predictions to return"
  }
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Analysis complete",
  "input_quality": "high",
  "extraction": {
    "symptoms": [
      {
        "canonical_name": "headache",
        "matched_variant": "headache",
        "confidence": 0.90,
        "severity": "severe",
        "duration": null,
        "negated": false
      },
      {
        "canonical_name": "fever",
        "matched_variant": "fever",
        "confidence": 0.90,
        "severity": "mild",
        "duration": "3 days",
        "negated": false
      },
      {
        "canonical_name": "chest_pain",
        "matched_variant": "chest pain",
        "confidence": 0.95,
        "severity": "moderate",
        "duration": null,
        "negated": false
      }
    ],
    "confidence": {
      "overall": 0.85,
      "components": {
        "match_confidence": 0.92,
        "coverage_score": 0.45,
        "specificity_score": 0.75,
        "coherence_score": 0.67
      },
      "recommendation": "Good symptom description. Analysis is proceeding with moderate confidence."
    }
  },
  "predictions": [
    {
      "rank": 1,
      "disease": "Hypertension",
      "confidence": 0.8743,
      "severity": "Moderate",
      "description": "Hypertension (high blood pressure) is a common condition...",
      "treatment": "Consult a cardiologist. Monitor blood pressure regularly. Reduce salt intake...",
      "precautions": ["reduce salt intake", "exercise regularly", "maintain healthy weight", "avoid stress"],
      "matching_symptoms": ["headache", "chest_pain"]
    },
    {
      "rank": 2,
      "disease": "Common Cold",
      "confidence": 0.6234,
      "severity": "Mild",
      "description": "The common cold is a viral infection of your nose and throat...",
      "treatment": "Rest and hydration. Over-the-counter cold medications. Vitamin C supplements...",
      "precautions": ["wash hands regularly", "avoid close contact with sick individuals", "stay hydrated", "rest"],
      "matching_symptoms": ["fever", "headache"]
    },
    {
      "rank": 3,
      "disease": "Heart Attack",
      "confidence": 0.1456,
      "severity": "Severe",
      "description": "A heart attack occurs when the flow of blood to the heart is blocked...",
      "treatment": "EMERGENCY: Call emergency services immediately. Do not drive yourself...",
      "precautions": ["maintain healthy diet", "exercise regularly", "avoid smoking", "control blood pressure"],
      "matching_symptoms": ["chest_pain"]
    }
  ],
  "disclaimer": "This analysis is for informational purposes only and does not constitute medical advice. Please consult a healthcare professional for proper diagnosis and treatment.",
  "timestamp": "2024-06-15T14:30:00Z",
  "request_id": "req_abc123xyz"
}
```

**Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Invalid input: description must be at least 10 characters",
  "error_code": "INVALID_INPUT",
  "timestamp": "2024-06-15T14:30:00Z",
  "request_id": "req_def456uvw"
}
```

**Response (422 Unprocessable Entity - Low Confidence):**
```json
{
  "status": "insufficient_input",
  "message": "Please provide more specific symptoms for a reliable analysis.",
  "extraction": {
    "symptoms": [],
    "confidence": {
      "overall": 0.0,
      "recommendation": "Please provide more specific symptoms. Try describing physical symptoms like pain, fever, cough, or rash."
    }
  },
  "predictions": null,
  "timestamp": "2024-06-15T14:30:00Z"
}
```

### 7.6.7 Endpoint: `/api/predict` (Structured)

**Purpose:** Accept a pre-structured list of symptoms (e.g., from a frontend checklist interface) and return disease predictions without NLP processing. This endpoint is useful for direct symptom selection interfaces where users select symptoms from a predefined list.

**Request:**
```bash
POST /api/predict
Content-Type: application/json

{
  "symptoms": ["fever", "cough", "shortness_of_breath", "chest_pain"],
  "user_id": "optional_user_id",
  "return_top_k": 3
}
```

**Request Body Schema:**
```json
{
  "symptoms": {
    "type": "array",
    "items": {"type": "string"},
    "required": true,
    "minItems": 3,
    "maxItems": 15,
    "description": "List of canonical symptom identifiers"
  },
  "user_id": {
    "type": "string",
    "required": false
  },
  "return_top_k": {
    "type": "integer",
    "required": false,
    "default": 3,
    "minimum": 1,
    "maximum": 5
  }
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "symptoms": ["fever", "cough", "shortness_of_breath", "chest_pain"],
  "predictions": [
    {
      "rank": 1,
      "disease": "Pneumonia",
      "confidence": 0.9123,
      "severity": "Severe",
      "description": "Pneumonia is an infection that inflames the air sacs in one or both lungs...",
      "treatment": "Consult a pulmonologist. Antibiotics for bacterial pneumonia. Rest and hydration...",
      "precautions": ["get vaccinated", "practice good hygiene", "don't smoke", "eat healthy"]
    },
    {
      "rank": 2,
      "disease": "Asthma",
      "confidence": 0.4521,
      "severity": "Moderate",
      "description": "Asthma is a condition in which your airways narrow and swell...",
      "treatment": "Use inhaler as prescribed. Avoid triggers. Consult a pulmonologist...",
      "precautions": ["avoid allergens", "use air purifier", "keep inhaler handy", "regular checkups"]
    },
    {
      "rank": 3,
      "disease": "Heart Attack",
      "confidence": 0.2345,
      "severity": "Severe",
      "description": "A heart attack occurs when the flow of blood to the heart is blocked...",
      "treatment": "EMERGENCY: Call emergency services immediately...",
      "precautions": ["maintain healthy diet", "exercise regularly", "avoid smoking", "control blood pressure"]
    }
  ],
  "disclaimer": "This prediction is for informational purposes only...",
  "timestamp": "2024-06-15T14:30:00Z",
  "request_id": "req_ghi789rst"
}
```

### 7.6.8 Error Handling and Status Codes

The API implements a consistent error response format across all endpoints:

| HTTP Status | Error Code | Description | Client Action |
|-------------|------------|-------------|---------------|
| 200 | — | Success | Process response |
| 400 | INVALID_INPUT | Malformed request or validation failure | Correct input and retry |
| 401 | UNAUTHORIZED | Authentication required | Provide valid credentials |
| 403 | FORBIDDEN | Insufficient permissions | Contact administrator |
| 404 | NOT_FOUND | Requested resource does not exist | Verify endpoint URL |
| 422 | INSUFFICIENT_INPUT | Extraction confidence too low | Request more detailed symptoms |
| 500 | INTERNAL_ERROR | Server-side processing error | Retry with exponential backoff |
| 503 | SERVICE_UNAVAILABLE | Dependency failure (database, model) | Retry after delay |

```python
# Unified error response format
error_response = {
    "status": "error",
    "message": "Human-readable error description",
    "error_code": "MACHINE_READABLE_ERROR_CODE",
    "timestamp": datetime.utcnow().isoformat(),
    "request_id": generate_request_id(),
    "details": {}  # Optional additional context
}
```

## 7.7 Request Lifecycle

The complete lifecycle of an API request from initial reception to final response involves multiple processing stages, each with specific responsibilities and error handling requirements.

### 7.7.1 Request Lifecycle Stages

```python
def handle_analyze_request():
    """
    Complete request lifecycle for /api/analyze endpoint.
    """
    # Stage 1: Request Reception
    request_id = generate_request_id()
    start_time = time.time()
    
    try:
        # Stage 2: Input Validation
        data = request.get_json()
        validate_request(data, schema=ANALYZE_SCHEMA)
        
        # Stage 3: Authentication (if required)
        user = authenticate_user(request.headers.get('Authorization'))
        
        # Stage 4: Rate Limiting Check
        check_rate_limit(request.remote_addr, user)
        
        # Stage 5: NLP Processing
        extraction_result = nlp_engine.extract_symptoms(data['description'])
        
        # Stage 6: Confidence Check
        if extraction_result['confidence']['overall'] < 0.4:
            return build_response(422, INSUFFICIENT_INPUT, extraction_result)
        
        # Stage 7: Feature Vector Construction
        feature_vector = build_tfidf_vector(extraction_result['symptoms'])
        
        # Stage 8: ML Prediction
        predictions = ml_predictor.predict(feature_vector, top_k=data.get('return_top_k', 3))
        
        # Stage 9: Disease Information Enrichment
        enriched_predictions = enrich_predictions(predictions)
        
        # Stage 10: Audit Logging
        log_prediction(request_id, user, data, extraction_result, predictions)
        
        # Stage 11: Response Assembly
        response = build_success_response(
            extraction=extraction_result,
            predictions=enriched_predictions,
            request_id=request_id
        )
        
        # Stage 12: Performance Metrics
        record_latency(request_id, time.time() - start_time)
        
        return response
        
    except ValidationError as e:
        return build_response(400, INVALID_INPUT, details=e.errors)
    except RateLimitExceeded as e:
        return build_response(429, RATE_LIMITED, retry_after=e.retry_after)
    except ModelLoadError as e:
        return build_response(503, SERVICE_UNAVAILABLE, details=str(e))
    except Exception as e:
        log_error(request_id, e)
        return build_response(500, INTERNAL_ERROR)
```

## 7.8 Conclusion

The system design of the Smart Medical Assistant establishes a robust, modular architecture that separates concerns across the frontend, backend, and data layers. The RESTful API design provides a clean, predictable interface for client applications, while the modular component architecture enables independent development, testing, and deployment of each subsystem. The technology stack is selected for its maturity, ecosystem support, and alignment with the project's requirements, ensuring that the system can be developed efficiently and deployed reliably.

The comprehensive API specification ensures that frontend developers have a clear contract for integration, while the error handling and request lifecycle documentation provides operations teams with the information needed to monitor and troubleshoot the system in production. The CORS-enabled API design supports multiple frontend deployment scenarios, from local development to production web applications, without requiring backend modifications.
