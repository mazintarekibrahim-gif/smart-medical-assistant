# Chapter 10: System Architecture and Deployment

## 10.1 Introduction

The system architecture of the Smart Medical Assistant defines the structural organization of the software system, the allocation of components to hardware and software infrastructure, and the strategies for ensuring security, scalability, and maintainability. This chapter presents the comprehensive architecture specification, including the three-tier architecture breakdown, deployment topology, security considerations, and scalability planning. The architecture is designed to support the current graduation project requirements while providing a foundation for future enhancements and production deployment.

## 10.2 Three-Tier Architecture

The Smart Medical Assistant adopts a classic three-tier architecture, which separates the application into distinct layers: the Presentation Tier (frontend), the Application Tier (backend), and the Data Tier (database). This separation provides multiple benefits: independent development and deployment of each tier, improved security through layered defense, and scalable resource allocation based on the demands of each tier.

### 10.2.1 Architecture Overview

```
+-----------------------------------------------------------------------------+
|                         THREE-TIER ARCHITECTURE                             |
+-----------------------------------------------------------------------------+

  +---------------------------+      +---------------------------+      +---------------------------+
  |   PRESENTATION TIER       |      |   APPLICATION TIER        |      |   DATA TIER               |
  |   (Frontend Layer)          |      |   (Backend Layer)           |      |   (Database Layer)        |
  +---------------------------+      +---------------------------+      +---------------------------+
  |                           |      |                           |      |                           |
  |  +---------------------+  |      |  +---------------------+  |      |  +---------------------+  |
  |  | HTML5 Structure     |  |      |  | Flask API Server    |  |      |  | MySQL 8.0 Server    |  |
  |  | Semantic markup     |  |      |  | Python 3.9+         |  |      |  | InnoDB Engine       |  |
  |  | Accessibility (A11y)|  |      |  | WSGI/Gunicorn       |  |      |  | ACID Transactions   |  |
  |  +---------------------+  |      |  +---------------------+  |      |  +---------------------+  |
  |                           |      |                           |      |                           |
  |  +---------------------+  |      |  +---------------------+  |      |  +---------------------+  |
  |  | CSS3 Styling        |  |      |  | NLP Engine          |  |      |  | Disease Reference   |  |
  |  | Flexbox/Grid layouts|  |      |  | NLTK, regex         |  |      |  | Data (30 diseases)  |  |
  |  | Responsive design   |  |      |  | Symptom extraction  |  |      |  | Symptom Vocabulary  |  |
  |  | Animations/Transitions|  |    |  | Pattern matching    |  |      |  | Medical Advice      |  |
  |  +---------------------+  |      |  +---------------------+  |      |  +---------------------+  |
  |                           |      |                           |      |                           |
  |  +---------------------+  |      |  +---------------------+  |      |  +---------------------+  |
  |  | JavaScript Logic    |  |      |  | ML Predictor        |  |      |  | User Accounts       |  |
  |  | DOM manipulation    |  |      |  | XGBoost Classifier  |  |      |  | Prediction History  |  |
  |  | Fetch API calls     |  |      |  | TF-IDF Vectorizer   |  |      |  | Audit Logs          |  |
  |  | Form validation     |  |      |  | Label Encoder       |  |      |  | Feedback Records    |  |
  |  | Result rendering    |  |      |  | Feature pipeline    |  |      |  +---------------------+  |
  |  +---------------------+  |      |  +---------------------+  |      |                           |
  |                           |      |                           |      |                           |
  |  +---------------------+  |      |  +---------------------+  |      |                           |
  |  | Chart.js (optional) |  |      |  | Authentication      |  |      |                           |
  |  | Data visualization  |  |      |  | Werkzeug security   |  |      |                           |
  |  +---------------------+  |      |  | Session management  |  |      |                           |
  |                           |      |  +---------------------+  |      |                           |
  +---------------------------+      +---------------------------+      +---------------------------+
            |                                    |                                    |
            | HTTP/HTTPS                         | SQLAlchemy / PyMySQL               | TCP/IP
            | (REST API)                         | (ORM / Raw SQL)                    | (Port 3306)
            |                                    |                                    |
            v                                    v                                    v
     +---------------------------------------------------------------+
     |                         COMMUNICATION PROTOCOLS                 |
     |  Frontend → Backend: JSON over HTTP/HTTPS (REST API)            |
     |  Backend → Database: SQL via SQLAlchemy ORM or raw SQL          |
     |  Backend → Model Files: File system I/O (joblib serialization)  |
     +---------------------------------------------------------------+
```

### 10.2.2 Presentation Tier (Frontend Layer)

The Presentation Tier is responsible for rendering the user interface and handling user interactions. It communicates with the Application Tier exclusively through the REST API defined in Chapter 7.

**Technology Stack:**

| Component | Technology | Role |
|-----------|-----------|------|
| Markup | HTML5 | Semantic document structure, form elements, accessibility attributes |
| Styling | CSS3 | Visual presentation, responsive layouts, animations, theme consistency |
| Logic | JavaScript (ES6+) | Client-side interactivity, API communication, dynamic content rendering |
| Icons | Font Awesome 6 | Medical and UI iconography |
| Fonts | Google Fonts (Inter, Roboto) | Typography for readability and professional appearance |

**Key Responsibilities:**

1. **User Input Collection**: Provide intuitive forms for natural language symptom description and structured symptom selection from categorized checklists.

2. **Input Validation**: Perform client-side validation (minimum length, maximum length, character filtering) before submitting to the API to improve user experience and reduce unnecessary server requests.

3. **API Integration**: Use the native Fetch API to communicate with the Flask backend, handling JSON request/response payloads, loading states, and error conditions gracefully.

4. **Result Presentation**: Render prediction results as visually distinct cards showing predicted disease, confidence level, severity indicator, description, treatment recommendations, and precautionary measures. Apply color coding (green for mild, yellow for moderate, red for severe) for immediate visual comprehension.

5. **Responsive Design**: Ensure the interface is functional and visually appealing across devices (desktop, tablet, mobile) using CSS media queries and flexbox/grid layouts.

6. **Accessibility Compliance**: Implement ARIA labels, keyboard navigation, screen reader support, and sufficient color contrast to meet WCAG 2.1 Level AA standards.

### 10.2.3 Application Tier (Backend Layer)

The Application Tier is the computational core of the system, hosting the Flask web server, NLP engine, machine learning pipeline, and authentication service. It processes requests from the Presentation Tier, orchestrates data flows between components, and persists data to the Data Tier.

**Technology Stack:**

| Component | Technology | Role |
|-----------|-----------|------|
| Web Framework | Flask 2.3.x | HTTP request routing, middleware, request/response handling |
| WSGI Server | Gunicorn 21.x | Production-grade WSGI server with multi-worker process model |
| NLP Engine | Python 3.9, NLTK 3.8 | Symptom extraction, text normalization, attribute detection |
| ML Pipeline | scikit-learn 1.3, XGBoost 1.7 | Feature vectorization, disease classification, prediction probability |
| ORM | SQLAlchemy 2.0 | Database abstraction, model definitions, query building |
| Authentication | Werkzeug Security | Password hashing, session token management |
| Data Processing | pandas 2.0, NumPy 1.24 | Data manipulation, numerical operations, array handling |
| Serialization | joblib 1.3 | Model persistence and deserialization |

**Key Responsibilities:**

1. **HTTP API Serving**: Expose RESTful endpoints for health checks, symptom analysis, disease queries, user authentication, and feedback collection. Handle CORS, content negotiation, and error response formatting.

2. **Request Processing Pipeline**: For each `/api/analyze` request, execute the sequential processing pipeline: input validation → NLP extraction → confidence checking → feature vectorization → ML prediction → database enrichment → response assembly → audit logging.

3. **Natural Language Processing**: Convert free-text user descriptions into structured, canonical symptom representations using the domain-specific NLP engine described in Chapter 6.

4. **Machine Learning Inference**: Transform structured symptom data into TF-IDF feature vectors and apply the trained XGBoost classifier to produce disease probability distributions.

5. **User Authentication**: Manage user registration, login, session validation, and password security using industry-standard hashing algorithms (Werkzeug's pbkdf2:sha256).

6. **Audit Logging**: Record every prediction request, including input text, extracted symptoms, predicted diseases, confidence scores, timestamps, and user feedback, to enable model performance monitoring and continuous improvement.

### 10.2.4 Data Tier (Database Layer)

The Data Tier provides persistent storage for all structured data required by the system. It uses MySQL 8.0 with the InnoDB storage engine, ensuring ACID compliance, transactional integrity, and referential constraint enforcement.

**Technology Stack:**

| Component | Technology | Role |
|-----------|-----------|------|
| Database Server | MySQL 8.0 | Relational database management system |
| Storage Engine | InnoDB | Transactional storage with row-level locking and foreign key support |
| Driver | PyMySQL 1.1 | Pure Python MySQL client for database connectivity |
| ORM | SQLAlchemy 2.0 | Object-relational mapping for database abstraction |
| Schema | UTF-8 (utf8mb4) | Full Unicode support including medical symbols and international text |

**Key Responsibilities:**

1. **User Data Management**: Store user account information, authentication credentials, profile data, and login history securely.

2. **Disease Reference Storage**: Maintain the master catalog of 30 diseases, including descriptions, severity classifications, recommended treatments, and precautionary measures.

3. **Symptom Vocabulary Management**: Store the canonical symptom dictionary with 62+ entries, including category classifications, body system associations, and common variant names.

4. **Prediction History**: Log every prediction request with full traceability: input text, extracted symptoms, prediction results, confidence scores, model version, and user feedback.

5. **Medical Advice Association**: Store disease-specific advice entries categorized by type (lifestyle, diet, exercise, medication, emergency), enabling flexible and extensible recommendation delivery.

## 10.5 Deployment Architecture

The deployment architecture specifies how the three-tier system is mapped to physical or virtual infrastructure, including server roles, network configuration, and service orchestration.

### 10.5.1 Single-Server Deployment (Development / Small Scale)

For development environments and small-scale deployments, all components can run on a single server:

```
+-----------------------------------------------------------------------------+
|                    SINGLE-SERVER DEPLOYMENT                                 |
|                         (Development / Small Scale)                         |
+-----------------------------------------------------------------------------+

     +---------------------+
     |    Internet         |
     +----------+----------+
                |
                | HTTPS (443)
                v
     +---------------------+     +---------------------+     +---------------------+
     |    Nginx            |     |    Nginx            |     |    Nginx            |
     |  Reverse Proxy      |---->|  Static Files       |     |  SSL Termination    |
     |  + Load Balancer    |     |  (HTML/CSS/JS)      |     |  (Let's Encrypt)    |
     +----------+----------+     +---------------------+     +---------------------+
                |
                | HTTP (5000) / UNIX Socket
                v
     +---------------------+
     |    Gunicorn         |
     |  (4-8 workers)      |
     |  Flask Application  |
     +----------+----------+
                |
                | SQL (3306) / UNIX Socket
                v
     +---------------------+
     |    MySQL 8.0        |
     |  (Local Instance)   |
     +---------------------+

     Server Specifications (Minimum):
     - CPU: 2 cores
     - RAM: 4 GB
     - Storage: 20 GB SSD
     - OS: Ubuntu 22.04 LTS
```

### 10.5.2 Production Deployment Architecture

For production environments with higher availability requirements, a multi-server architecture is recommended:

```
+-----------------------------------------------------------------------------+
|                    PRODUCTION DEPLOYMENT ARCHITECTURE                       |
+-----------------------------------------------------------------------------+

                                    +------------------+
                                    |   Load Balancer  |
                                    |   (Nginx / HAProxy) |
                                    |   - SSL termination |
                                    |   - Rate limiting   |
                                    |   - Health checks   |
                                    +--------+---------+
                                             |
                              +--------------+--------------+
                              |                             |
                              v                             v
                    +------------------+         +------------------+
                    |   App Server 1   |         |   App Server 2   |
                    |   (Gunicorn)     |         |   (Gunicorn)     |
                    |   Flask + ML     |         |   Flask + ML     |
                    |   + NLP          |         |   + NLP          |
                    +--------+---------+         +--------+---------+
                             |                             |
                             +--------------+--------------+
                                            |
                                            | SQL
                                            v
                              +---------------------------+
                              |    MySQL Primary          |
                              |    (Read/Write)           |
                              +-------------+-------------+
                                            |
                                            | Replication
                                            v
                              +---------------------------+
                              |    MySQL Replica          |
                              |    (Read-Only)            |
                              +---------------------------+

     +------------------+         +------------------+         +------------------+
     |   File Storage   |         |   Cache Layer    |         |   Monitoring     |
     |   (Model Files)  |         |   (Redis /       |         |   (Prometheus +  |
     |   - Shared NFS   |         |    Memcached)    |         |    Grafana)      |
     |   - Backup storage |       |   - Session store |         |   - Metrics      |
     +------------------+         |   - Rate limit   |         |   - Alerting     |
                                  |     counters     |         |   - Dashboards   |
                                  +------------------+         +------------------+
```

### 10.5.3 Docker Containerization

For consistent deployment across environments, the following Docker architecture is defined:

```dockerfile
# Dockerfile: Flask Application
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=mysql+pymysql://user:pass@db:3306/medical_assistant
      - MODEL_PATH=/app/models/xgb_pipeline.pkl
    depends_on:
      - db
    volumes:
      - ./models:/app/models:ro
    restart: unless-stopped

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root_password
      - MYSQL_DATABASE=medical_assistant
      - MYSQL_USER=user
      - MYSQL_PASSWORD=pass
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped

  nginx:
    image: nginx:1.24
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./frontend:/usr/share/nginx/html:ro
      - ./certbot-data:/etc/letsencrypt:ro
    depends_on:
      - web
    restart: unless-stopped

volumes:
  mysql_data:
```

## 10.6 Security Considerations

Security is a critical concern for any system handling health-related information. The Smart Medical Assistant implements defense-in-depth security measures across all tiers.

### 10.6.1 Authentication and Authorization

| Security Measure | Implementation | Description |
|-----------------|----------------|-------------|
| **Password Hashing** | Werkzeug `generate_password_hash` (pbkdf2:sha256, 150,000 iterations) | One-way password hashing with salt |
| **Session Management** | JWT tokens or Flask-Login sessions | Stateless or stateful session management with expiry |
| **Input Sanitization** | HTML escaping, parameterized queries | Prevention of XSS and SQL injection |
| **Rate Limiting** | Flask-Limiter (Redis backend) | 100 requests per minute per IP, 10 per second per user |
| **CORS Policy** | Explicit origin whitelist | Only trusted domains can access the API |

### 10.6.2 Data Protection

| Security Measure | Implementation | Description |
|-----------------|----------------|-------------|
| **Transport Encryption** | TLS 1.2+ (HTTPS) | All client-server communication encrypted |
| **Database Encryption** | MySQL InnoDB tablespace encryption | At-rest encryption for sensitive data |
| **PII Handling** | Pseudonymization | User IDs replace direct identifiers in logs |
| **Backup Encryption** | AES-256 | Encrypted database backups |

### 10.6.3 Application Security

| Security Measure | Implementation | Description |
|-----------------|----------------|-------------|
| **Input Validation** | JSON Schema validation | Strict request payload validation |
| **Error Handling** | Generic error messages | Internal details never exposed to clients |
| **Dependency Management** | pip-audit, safety | Regular vulnerability scanning |
| **Logging** | Structured audit logs | All access and prediction requests logged |

### 10.6.4 Medical Data Disclaimers

The system includes explicit disclaimers at every user touchpoint:

- **Input Form**: "This tool is for informational purposes only and does not replace professional medical advice."
- **Results Page**: "The predicted conditions are based on symptom pattern matching and should be verified by a healthcare professional."
- **Severe Conditions**: "This condition may be serious. Please seek immediate medical attention."
- **API Response**: `"disclaimer": "This analysis is for informational purposes only..."`

## 10.7 Scalability Notes

### 10.7.1 Horizontal Scaling Strategy

The three-tier architecture supports horizontal scaling at each layer:

**Presentation Tier Scaling:**
- Static frontend assets (HTML/CSS/JS) are served by Nginx, which handles high concurrency efficiently.
- CDN integration (e.g., CloudFlare) can cache static assets at edge locations for global distribution.

**Application Tier Scaling:**
- Gunicorn workers can be increased based on CPU core count (typically 2-4 workers per core).
- Multiple application servers can be deployed behind a load balancer (Nginx or HAProxy) with health checks.
- The ML model is stateless and can be loaded on each application server; no shared session state is required.

**Data Tier Scaling:**
- MySQL primary-replica replication enables read scaling (queries can be directed to replicas).
- For write scaling, consider MySQL partitioning by date or user ID for the Predictions table.
- Connection pooling (SQLAlchemy `pool_size=10`, `max_overflow=20`) prevents connection exhaustion.

### 10.7.2 Performance Benchmarks

| Metric | Target | Notes |
|--------|--------|-------|
| **API Response Time (P50)** | < 200 ms | 50th percentile for `/api/predict` with structured input |
| **API Response Time (P95)** | < 500 ms | 95th percentile for `/api/analyze` with NLP processing |
| **NLP Processing Time** | < 100 ms | Symptom extraction from typical user description |
| **ML Inference Time** | < 50 ms | XGBoost prediction for single feature vector |
| **Database Query Time** | < 50 ms | Disease detail lookup with indexes |
| **Concurrent Users** | 100+ | Supported on single-server deployment with 4 workers |
| **Throughput** | 50 req/s | Sustained request rate on standard cloud instance |

### 10.7.3 Caching Strategy

| Cache Layer | Technology | Content | TTL | Invalidation |
|------------|-----------|---------|-----|-------------|
| **API Response** | Redis | Disease list, symptom list | 1 hour | Manual on data update |
| **Disease Details** | Redis | Individual disease records | 30 minutes | On MedicalAdvice update |
| **Model Predictions** | In-memory | Identical symptom set predictions | 5 minutes | Not applicable (deterministic) |
| **Session Data** | Redis | User session tokens | 24 hours | On logout |

### 10.7.4 Monitoring and Alerting

| Metric | Tool | Threshold | Alert |
|--------|------|-----------|-------|
| **API Error Rate** | Prometheus | > 5% | PagerDuty / Email |
| **Response Time P95** | Prometheus | > 1 second | Slack / Email |
| **Database Connections** | MySQL Metrics | > 80% of max | Email |
| **Disk Usage** | Node Exporter | > 85% | Email |
| **Model Accuracy Drift** | Custom logging | F1 < 0.90 | Email to ML team |
| **Failed Login Attempts** | Application logs | > 10 per minute | Security alert |

## 10.8 Environment Configuration

The system supports three runtime environments with configuration managed through environment variables:

### 10.8.1 Environment Variables

| Variable | Development | Staging | Production | Description |
|----------|-------------|----------|------------|-------------|
| `FLASK_ENV` | development | production | production | Flask environment mode |
| `FLASK_DEBUG` | True | False | False | Debug mode flag |
| `DATABASE_URL` | sqlite:///dev.db | mysql://staging/... | mysql://production/... | Database connection string |
| `MODEL_PATH` | ./models/ | ./models/ | /app/models/ | Path to serialized model files |
| `SECRET_KEY` | dev-secret-key | staging-secret | <random-256-bit> | Flask secret key for sessions |
| `CORS_ORIGINS` | * | https://staging.example.com | https://example.com | Allowed CORS origins |
| `RATE_LIMIT` | 1000/minute | 100/minute | 100/minute | API rate limit |
| `LOG_LEVEL` | DEBUG | INFO | WARNING | Python logging level |

## 10.9 Conclusion

The system architecture of the Smart Medical Assistant is designed as a production-ready, three-tier web application that separates concerns across the presentation, application, and data layers. The frontend employs modern HTML5/CSS3/JS technologies with a responsive, accessible design. The backend leverages Flask as a lightweight yet powerful web framework, integrating a domain-specific NLP engine and a high-performance XGBoost classifier for disease prediction. The data layer uses MySQL 8.0 with InnoDB for reliable, transactional data persistence.

The deployment architecture supports both single-server development setups and multi-server production configurations, with Docker containerization ensuring environment consistency. Security is addressed through multiple layers: password hashing, transport encryption, input sanitization, rate limiting, and comprehensive audit logging. Scalability is achieved through horizontal scaling of stateless application servers, database replication for read scaling, and caching layers for frequently accessed reference data.

The architecture is intentionally conservative in technology selection, prioritizing stability, maintainability, and team familiarity over novel frameworks. This approach ensures that the system can be reliably developed, deployed, and maintained within the scope of a graduation project while providing a solid foundation for future production deployment. The explicit medical disclaimers throughout the system underscore its role as a decision-support tool rather than a diagnostic replacement, aligning with ethical and legal requirements for health-related software applications.
