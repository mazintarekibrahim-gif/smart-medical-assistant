# Chapter 8: Database Design

## 8.1 Introduction

The database layer of the Smart Medical Assistant provides persistent storage for user accounts, disease reference information, prediction history, and medical advice content. The database schema is designed to support the core functionality of the application while maintaining data integrity, query performance, and extensibility for future enhancements. This chapter presents the complete Entity-Relationship Diagram (ERD), table schemas, SQL CREATE TABLE statements, relationship definitions, and performance optimization strategies for the MySQL database.

The database design follows the principles of third normal form (3NF) where appropriate, while selectively denormalizing certain reference tables (such as disease descriptions) to improve read performance for the most common query patterns. The schema supports user authentication, prediction logging, disease information retrieval, and medical advice association, providing a complete data foundation for the Smart Medical Assistant system.

## 8.2 Entity-Relationship Diagram

The following text-based ERD illustrates the relationships between the five primary entities in the database: Users, Symptoms, Diseases, Predictions, and MedicalAdvice.

### 8.2.1 Entity-Relationship Diagram (ASCII)

```
+-----------------------------------------------------------------------------+
|                         ENTITY-RELATIONSHIP DIAGRAM                       |
+-----------------------------------------------------------------------------+

+----------------+          +----------------+          +----------------+
|     USERS      |          |   PREDICTIONS  |          |    DISEASES    |
+----------------+          +----------------+          +----------------+
| PK user_id     |<|------o| FK user_id     |          | PK disease_id  |
|    username    |          | PK prediction_id|         |    name        |
|    email       |          |    input_text  |          |    severity    |
|    password_hash|         |    predicted_disease    |    description |
|    full_name   |          |    confidence  |          |    treatment   |
|    age         |          |    input_type  |          |    precautions |
|    gender      |          |    timestamp   |          |    category    |
|    created_at  |          |    nlp_confidence       |    created_at  |
|    updated_at  |          |    top_3_results        |    updated_at  |
|    is_active   |          |    user_feedback        |                |
|    last_login  |          |    ip_address  |          |                |
+----------------+          +----------------+          +----------------+
         |                           |                           |
         |                           |                           |
         |                    +------+------+                    |
         |                    |             |                     |
         |                    v             v                     |
         |          +----------------+   +----------------+     |
         |          | SYMPTOMS_LOG   |   | MEDICAL_ADVICE |     |
         |          +----------------+   +----------------+     |
         |          | PK log_id      |   | PK advice_id   |     |
         |          | FK prediction_id|   | FK disease_id  |<----+-----+
         |          | FK symptom_id  |   |    advice_type |     |     |
         |          |    severity    |   |    content     |     |     |
         |          |    is_negated  |   |    severity_level     |     |
         |          |    duration    |   |    created_at  |     |     |
         |          |    confidence  |   |    updated_at  |     |     |
         |          +----------------+   +----------------+     |     |
         |                                                    |     |
         |                                                    v     v
         |                                          +----------------+
         |                                          |    SYMPTOMS    |
         |                                          +----------------+
         |                                          | PK symptom_id  |
         |                                          |    name        |
         |                                          |    category    |
         |                                          |    description |
         |                                          |    body_system |
         |                                          |    is_active   |
         |                                          |    created_at  |
         |                                          |    updated_at  |
         |                                          +----------------+
         |                                                    |
         |                                                    |
         |                                          +----------------+
         |                                          | DISEASE_SYMPTOM|
         |                                          | (Junction)     |
         |                                          +----------------+
         |                                          | PK ds_id       |
         |                                          | FK disease_id  |
         |                                          | FK symptom_id  |
         |                                          |    frequency   |
         |                                          |    is_required |
         |                                          +----------------+
         |                                                    |
         +----------------------------------------------------+
                              |
                              |
                              v
+-----------------------------------------------------------------------------+
| RELATIONSHIP SUMMARY                                                        |
|                                                                             |
| USERS (1) ----<o PREDICTIONS (>1)   : One user can have many predictions   |
| PREDICTIONS (1) --<o SYMPTOMS_LOG (>1) : One prediction logs many symptoms  |
| DISEASES (1) ----<o PREDICTIONS (>0) : One disease can be predicted many    |
|                                        times (via predicted_disease)       |
| DISEASES (1) ----<o MEDICAL_ADVICE (>1) : One disease has multiple advice   |
|                                           entries                          |
| DISEASES (1) ----<o DISEASE_SYMPTOM (>1) : One disease has many symptoms   |
| SYMPTOMS (1) ----<o DISEASE_SYMPTOM (>1) : One symptom appears in many     |
|                                            diseases                        |
| SYMPTOMS (1) ----<o SYMPTOMS_LOG (>0) : One symptom appears in many logs   |
+-----------------------------------------------------------------------------+
```

### 8.2.2 Entity Definitions

| Entity | Description | Primary Key | Record Count (Expected) |
|--------|-------------|------------|----------------------|
| **Users** | Registered user accounts | user_id (INT, AUTO_INCREMENT) | 1,000+ |
| **Symptoms** | Canonical symptom definitions | symptom_id (INT, AUTO_INCREMENT) | 62 |
| **Diseases** | Disease reference information | disease_id (INT, AUTO_INCREMENT) | 30 |
| **Predictions** | User prediction history | prediction_id (INT, AUTO_INCREMENT) | 10,000+ |
| **MedicalAdvice** | Disease-specific medical advice | advice_id (INT, AUTO_INCREMENT) | 90+ |
| **SymptomsLog** | Log of symptoms per prediction | log_id (INT, AUTO_INCREMENT) | 50,000+ |
| **DiseaseSymptom** | Junction table for disease-symptom associations | ds_id (INT, AUTO_INCREMENT) | 500+ |

## 8.3 Table Schemas

### 8.3.1 Users Table

The Users table stores registered user account information, supporting authentication, profile management, and prediction history tracking.

```sql
-- Table: Users
-- Purpose: Store registered user accounts
-- Expected Records: 1,000+

CREATE TABLE Users (
    user_id         INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50) NOT NULL UNIQUE,
    email           VARCHAR(255) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    full_name       VARCHAR(100),
    age             INT CHECK (age >= 0 AND age <= 120),
    gender          ENUM('male', 'female', 'other', 'prefer_not_to_say') DEFAULT 'prefer_not_to_say',
    phone           VARCHAR(20),
    address         TEXT,
    profile_picture VARCHAR(255),        -- URL to profile image
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active       BOOLEAN DEFAULT TRUE,
    is_verified     BOOLEAN DEFAULT FALSE, -- Email verification status
    last_login      TIMESTAMP NULL,
    login_count     INT DEFAULT 0,
    failed_logins   INT DEFAULT 0,       -- For security lockout
    lockout_until   TIMESTAMP NULL,      -- Account lockout expiry
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_created_at (created_at),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Registered user accounts for the Smart Medical Assistant';
```

**Schema Details:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| user_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| username | VARCHAR(50) | NOT NULL, UNIQUE | Public display name |
| email | VARCHAR(255) | NOT NULL, UNIQUE | Login credential and communication |
| password_hash | VARCHAR(255) | NOT NULL | BCrypt-hashed password (never stored plaintext) |
| full_name | VARCHAR(100) | NULL | User's full name |
| age | INT | CHECK (0-120) | User age for demographic analysis |
| gender | ENUM | DEFAULT 'prefer_not_to_say' | User gender for demographic analysis |
| phone | VARCHAR(20) | NULL | Contact phone number |
| address | TEXT | NULL | Physical address (optional) |
| profile_picture | VARCHAR(255) | NULL | URL to profile image file |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | Last modification timestamp |
| is_active | BOOLEAN | DEFAULT TRUE | Account status flag |
| is_verified | BOOLEAN | DEFAULT FALSE | Email verification status |
| last_login | TIMESTAMP | NULL | Most recent login timestamp |
| login_count | INT | DEFAULT 0 | Total successful login count |
| failed_logins | INT | DEFAULT 0 | Consecutive failed login attempts |
| lockout_until | TIMESTAMP | NULL | Account lockout expiry time |

### 8.3.2 Symptoms Table

The Symptoms table defines the canonical symptom vocabulary used by the NLP engine and machine learning model. It serves as the master reference for all symptom-related operations.

```sql
-- Table: Symptoms
-- Purpose: Canonical symptom definitions
-- Expected Records: 62

CREATE TABLE Symptoms (
    symptom_id      INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL UNIQUE,
    canonical_name  VARCHAR(100) NOT NULL UNIQUE,  -- Machine-readable identifier
    display_name    VARCHAR(100) NOT NULL,         -- User-friendly display name
    category        VARCHAR(50) NOT NULL,          -- e.g., 'general', 'cardiovascular', 'neurological'
    body_system     VARCHAR(50),                   -- e.g., 'respiratory', 'digestive', 'nervous'
    description     TEXT,                          -- Detailed description of the symptom
    severity_indicator BOOLEAN DEFAULT FALSE,       -- Whether this symptom indicates severity
    common_variants JSON,                          -- Array of alternative names (e.g., ["feverish", "febrile"])
    is_active       BOOLEAN DEFAULT TRUE,          -- Whether symptom is currently in use
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_category (category),
    INDEX idx_body_system (body_system),
    INDEX idx_is_active (is_active),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Canonical symptom definitions for the medical assistant system';
```

**Schema Details:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| symptom_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique symptom identifier |
| name | VARCHAR(100) | NOT NULL, UNIQUE | Canonical symptom name (snake_case) |
| canonical_name | VARCHAR(100) | NOT NULL, UNIQUE | Machine-readable identifier |
| display_name | VARCHAR(100) | NOT NULL | Human-readable display name |
| category | VARCHAR(50) | NOT NULL | Symptom category classification |
| body_system | VARCHAR(50) | NULL | Affected physiological system |
| description | TEXT | NULL | Detailed symptom description |
| severity_indicator | BOOLEAN | DEFAULT FALSE | Whether symptom indicates severe condition |
| common_variants | JSON | NULL | JSON array of alternative names |
| is_active | BOOLEAN | DEFAULT TRUE | Active status flag |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | Last modification timestamp |

### 8.3.3 Diseases Table

The Diseases table stores comprehensive reference information for each disease in the system, including descriptions, treatments, and precautions.

```sql
-- Table: Diseases
-- Purpose: Disease reference information
-- Expected Records: 30

CREATE TABLE Diseases (
    disease_id      INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL UNIQUE,
    display_name    VARCHAR(100) NOT NULL,
    severity        ENUM('Mild', 'Moderate', 'Severe') NOT NULL,
    description     TEXT NOT NULL,                   -- Detailed disease description
    treatment       TEXT NOT NULL,                   -- Recommended treatment approach
    precautions     JSON NOT NULL,                   -- Array of precautionary measures
    common_symptoms JSON,                          -- Array of most common symptom IDs
    category        VARCHAR(50),                   -- e.g., 'infectious', 'chronic', 'autoimmune'
    body_system     VARCHAR(50),                   -- Primary affected system
    specialist_type VARCHAR(50),                   -- Recommended specialist (e.g., 'Cardiologist', 'Dermatologist')
    is_contagious   BOOLEAN DEFAULT FALSE,          -- Whether the disease is contagious
    recovery_time   VARCHAR(50),                   -- Typical recovery duration
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_severity (severity),
    INDEX idx_category (category),
    INDEX idx_body_system (body_system),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Disease reference information for the medical assistant system';
```

**Schema Details:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| disease_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique disease identifier |
| name | VARCHAR(100) | NOT NULL, UNIQUE | Disease name (snake_case) |
| display_name | VARCHAR(100) | NOT NULL | Human-readable display name |
| severity | ENUM | NOT NULL | General severity classification |
| description | TEXT | NOT NULL | Detailed disease description |
| treatment | TEXT | NOT NULL | Recommended treatment approach |
| precautions | JSON | NOT NULL | JSON array of precautionary measures |
| common_symptoms | JSON | NULL | JSON array of most common symptom IDs |
| category | VARCHAR(50) | NULL | Disease category classification |
| body_system | VARCHAR(50) | NULL | Primary affected physiological system |
| specialist_type | VARCHAR(50) | NULL | Recommended medical specialist |
| is_contagious | BOOLEAN | DEFAULT FALSE | Contagiousness flag |
| recovery_time | VARCHAR(50) | NULL | Typical recovery duration |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | Last modification timestamp |

### 8.3.4 Predictions Table

The Predictions table logs every prediction made by the system, enabling user history tracking, model performance monitoring, and analytics.

```sql
-- Table: Predictions
-- Purpose: Log prediction requests and results
-- Expected Records: 10,000+

CREATE TABLE Predictions (
    prediction_id   INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT,                           -- NULL for anonymous users
    input_text      TEXT NOT NULL,                 -- Original user input
    input_type      ENUM('natural_language', 'structured_list') DEFAULT 'natural_language',
    predicted_disease VARCHAR(100) NOT NULL,       -- Primary predicted disease name
    predicted_disease_id INT,                      -- Foreign key to Diseases
    confidence      DECIMAL(5,4) NOT NULL,        -- Prediction confidence (0.0000 - 1.0000)
    nlp_confidence  DECIMAL(5,4),                 -- NLP extraction confidence
    top_3_results   JSON,                          -- JSON array of top 3 predictions with scores
    model_version   VARCHAR(20) DEFAULT '1.0.0',   -- Model version used for prediction
    processing_time_ms INT,                        -- Request processing time in milliseconds
    user_feedback   ENUM('accurate', 'inaccurate', 'uncertain', NULL) DEFAULT NULL,
    feedback_notes  TEXT,                          -- User feedback notes
    ip_address      VARCHAR(45),                 -- Client IP for analytics
    user_agent      VARCHAR(255),                  -- Client browser info
    timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE SET NULL,
    FOREIGN KEY (predicted_disease_id) REFERENCES Diseases(disease_id) ON DELETE SET NULL,
    
    INDEX idx_user_id (user_id),
    INDEX idx_predicted_disease (predicted_disease),
    INDEX idx_confidence (confidence),
    INDEX idx_timestamp (timestamp),
    INDEX idx_user_timestamp (user_id, timestamp),
    INDEX idx_model_version (model_version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Prediction history for the medical assistant system';
```

**Schema Details:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| prediction_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique prediction identifier |
| user_id | INT | FK → Users(user_id), ON DELETE SET NULL | Associated user (NULL for anonymous) |
| input_text | TEXT | NOT NULL | Original user input description |
| input_type | ENUM | DEFAULT 'natural_language' | Input format type |
| predicted_disease | VARCHAR(100) | NOT NULL | Primary predicted disease name |
| predicted_disease_id | INT | FK → Diseases(disease_id), ON DELETE SET NULL | Disease foreign key |
| confidence | DECIMAL(5,4) | NOT NULL | Prediction confidence score |
| nlp_confidence | DECIMAL(5,4) | NULL | NLP extraction confidence |
| top_3_results | JSON | NULL | JSON array of top 3 predictions |
| model_version | VARCHAR(20) | DEFAULT '1.0.0' | ML model version used |
| processing_time_ms | INT | NULL | Request processing time |
| user_feedback | ENUM | DEFAULT NULL | User feedback on accuracy |
| feedback_notes | TEXT | NULL | Additional feedback notes |
| ip_address | VARCHAR(45) | NULL | Client IP address |
| user_agent | VARCHAR(255) | NULL | Client browser user agent |
| timestamp | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Prediction timestamp |

### 8.3.5 MedicalAdvice Table

The MedicalAdvice table stores disease-specific medical advice, including lifestyle recommendations, dietary suggestions, and when to seek professional care.

```sql
-- Table: MedicalAdvice
-- Purpose: Disease-specific medical advice and recommendations
-- Expected Records: 90+ (3-4 advice entries per disease)

CREATE TABLE MedicalAdvice (
    advice_id       INT AUTO_INCREMENT PRIMARY KEY,
    disease_id      INT NOT NULL,
    advice_type     ENUM('lifestyle', 'diet', 'exercise', 'medication', 'when_to_see_doctor', 'prevention', 'emergency') NOT NULL,
    severity_level  ENUM('Mild', 'Moderate', 'Severe', 'All') DEFAULT 'All',
    title           VARCHAR(200) NOT NULL,
    content         TEXT NOT NULL,
    priority        INT DEFAULT 1,                -- Display order (1 = highest)
    is_urgent       BOOLEAN DEFAULT FALSE,          -- Whether this advice is urgent
    source_reference VARCHAR(255),                  -- Medical reference or source
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (disease_id) REFERENCES Diseases(disease_id) ON DELETE CASCADE,
    
    INDEX idx_disease_id (disease_id),
    INDEX idx_advice_type (advice_type),
    INDEX idx_severity_level (severity_level),
    INDEX idx_priority (priority),
    INDEX idx_is_active (is_active),
    INDEX idx_disease_type (disease_id, advice_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Disease-specific medical advice and recommendations';
```

**Schema Details:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| advice_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique advice identifier |
| disease_id | INT | NOT NULL, FK → Diseases(disease_id) | Associated disease |
| advice_type | ENUM | NOT NULL | Category of advice |
| severity_level | ENUM | DEFAULT 'All' | Applicable severity level |
| title | VARCHAR(200) | NOT NULL | Advice title |
| content | TEXT | NOT NULL | Detailed advice content |
| priority | INT | DEFAULT 1 | Display order priority |
| is_urgent | BOOLEAN | DEFAULT FALSE | Urgency flag |
| source_reference | VARCHAR(255) | NULL | Medical reference source |
| is_active | BOOLEAN | DEFAULT TRUE | Active status flag |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | Last modification timestamp |

### 8.3.6 Supporting Tables

#### SymptomsLog Table

```sql
-- Table: SymptomsLog
-- Purpose: Detailed log of symptoms extracted per prediction
-- Expected Records: 50,000+ (5-10 symptoms per prediction)

CREATE TABLE SymptomsLog (
    log_id          INT AUTO_INCREMENT PRIMARY KEY,
    prediction_id   INT NOT NULL,
    symptom_id      INT NOT NULL,
    matched_variant VARCHAR(100),                  -- The actual matched text variant
    severity        VARCHAR(20),                   -- Detected severity (mild, moderate, severe)
    duration        VARCHAR(50),                   -- Detected duration
    is_negated      BOOLEAN DEFAULT FALSE,          -- Whether symptom was negated
    extraction_confidence DECIMAL(5,4),            -- Confidence of this specific extraction
    position_start  INT,                           -- Start position in input text
    position_end    INT,                           -- End position in input text
    timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (prediction_id) REFERENCES Predictions(prediction_id) ON DELETE CASCADE,
    FOREIGN KEY (symptom_id) REFERENCES Symptoms(symptom_id) ON DELETE RESTRICT,
    
    INDEX idx_prediction_id (prediction_id),
    INDEX idx_symptom_id (symptom_id),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Detailed log of symptoms extracted per prediction request';
```

#### DiseaseSymptom Junction Table

```sql
-- Table: DiseaseSymptom
-- Purpose: Many-to-many relationship between diseases and symptoms
-- Expected Records: 500+ (15-20 symptoms per disease)

CREATE TABLE DiseaseSymptom (
    ds_id           INT AUTO_INCREMENT PRIMARY KEY,
    disease_id      INT NOT NULL,
    symptom_id      INT NOT NULL,
    frequency       DECIMAL(5,4),                  -- Frequency of symptom in disease (0.0000 - 1.0000)
    is_required     BOOLEAN DEFAULT FALSE,          -- Whether symptom is required for diagnosis
    is_distinguishing BOOLEAN DEFAULT FALSE,        -- Whether symptom distinguishes this disease
    severity_association VARCHAR(20),              -- Typical severity of this symptom in this disease
    notes           TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (disease_id) REFERENCES Diseases(disease_id) ON DELETE CASCADE,
    FOREIGN KEY (symptom_id) REFERENCES Symptoms(symptom_id) ON DELETE CASCADE,
    UNIQUE KEY idx_disease_symptom (disease_id, symptom_id),
    
    INDEX idx_disease_id (disease_id),
    INDEX idx_symptom_id (symptom_id),
    INDEX idx_frequency (frequency)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Junction table linking diseases with their associated symptoms';
```

## 8.4 Relationships and Foreign Keys

The database schema implements the following referential integrity constraints:

### 8.4.1 Foreign Key Relationships

| Parent Table | Child Table | Foreign Key | On Delete | On Update | Relationship Type |
|-------------|------------|-------------|-----------|-----------|-------------------|
| Users | Predictions | user_id | SET NULL | CASCADE | One-to-Many |
| Diseases | Predictions | predicted_disease_id | SET NULL | CASCADE | One-to-Many |
| Diseases | MedicalAdvice | disease_id | CASCADE | CASCADE | One-to-Many |
| Diseases | DiseaseSymptom | disease_id | CASCADE | CASCADE | One-to-Many |
| Symptoms | DiseaseSymptom | symptom_id | CASCADE | CASCADE | One-to-Many |
| Symptoms | SymptomsLog | symptom_id | RESTRICT | CASCADE | One-to-Many |
| Predictions | SymptomsLog | prediction_id | CASCADE | CASCADE | One-to-Many |

### 8.4.2 Relationship Semantics

- **Users → Predictions (One-to-Many)**: A registered user can have multiple prediction records in their history. When a user is deleted, their predictions remain (user_id set to NULL) to preserve historical analytics data.

- **Diseases → Predictions (One-to-Many)**: A disease can be predicted multiple times across different user requests. When a disease is deleted, predictions referencing it retain the disease name but lose the foreign key linkage (SET NULL).

- **Diseases → MedicalAdvice (One-to-Many)**: A disease can have multiple advice entries (e.g., diet advice, exercise advice, when to see a doctor). When a disease is deleted, all associated advice is automatically deleted (CASCADE).

- **Diseases ↔ Symptoms (Many-to-Many via DiseaseSymptom)**: A disease can have multiple symptoms, and a symptom can be associated with multiple diseases. The junction table includes additional metadata (frequency, required status) that enriches the relationship.

- **Predictions → SymptomsLog (One-to-Many)**: Each prediction generates a detailed log of extracted symptoms. When a prediction is deleted, its symptom logs are automatically deleted (CASCADE).

## 8.5 Indexes for Performance

### 8.5.1 Index Design Strategy

The index design follows a query-driven strategy, where indexes are created to optimize the most frequent and performance-critical query patterns. The primary indexing targets are:

1. **Foreign key columns**: All foreign key columns are indexed to support efficient JOIN operations.
2. **Filter columns**: Columns frequently used in WHERE clauses (e.g., severity, category, timestamp) are indexed.
3. **Sort columns**: Columns used in ORDER BY clauses (e.g., timestamp, priority) are indexed.
4. **Composite indexes**: Multi-column indexes are created for common query patterns involving multiple filter conditions.

### 8.5.2 Complete Index Listing

| Table | Index Name | Columns | Type | Purpose |
|-------|-----------|---------|------|---------|
| Users | PRIMARY | user_id | B-Tree | Primary key lookup |
| Users | idx_username | username | B-Tree, UNIQUE | Login by username |
| Users | idx_email | email | B-Tree, UNIQUE | Login by email |
| Users | idx_created_at | created_at | B-Tree | User registration trends |
| Users | idx_is_active | is_active | B-Tree | Active user filtering |
| Symptoms | PRIMARY | symptom_id | B-Tree | Primary key lookup |
| Symptoms | idx_name | name | B-Tree, UNIQUE | Symptom name lookup |
| Symptoms | idx_category | category | B-Tree | Category filtering |
| Symptoms | idx_body_system | body_system | B-Tree | Body system filtering |
| Symptoms | idx_is_active | is_active | B-Tree | Active symptom filtering |
| Diseases | PRIMARY | disease_id | B-Tree | Primary key lookup |
| Diseases | idx_name | name | B-Tree, UNIQUE | Disease name lookup |
| Diseases | idx_severity | severity | B-Tree | Severity filtering |
| Diseases | idx_category | category | B-Tree | Category filtering |
| Diseases | idx_body_system | body_system | B-Tree | Body system filtering |
| Predictions | PRIMARY | prediction_id | B-Tree | Primary key lookup |
| Predictions | idx_user_id | user_id | B-Tree | User history queries |
| Predictions | idx_predicted_disease | predicted_disease | B-Tree | Disease prediction analytics |
| Predictions | idx_confidence | confidence | B-Tree | Confidence-based filtering |
| Predictions | idx_timestamp | timestamp | B-Tree | Time-based queries |
| Predictions | idx_user_timestamp | user_id, timestamp | B-Tree, COMPOSITE | User history ordered by time |
| Predictions | idx_model_version | model_version | B-Tree | Model performance tracking |
| MedicalAdvice | PRIMARY | advice_id | B-Tree | Primary key lookup |
| MedicalAdvice | idx_disease_id | disease_id | B-Tree | Disease advice lookup |
| MedicalAdvice | idx_advice_type | advice_type | B-Tree | Advice type filtering |
| MedicalAdvice | idx_severity_level | severity_level | B-Tree | Severity-based filtering |
| MedicalAdvice | idx_priority | priority | B-Tree | Ordered display |
| MedicalAdvice | idx_disease_type | disease_id, advice_type | B-Tree, COMPOSITE | Specific advice retrieval |
| SymptomsLog | PRIMARY | log_id | B-Tree | Primary key lookup |
| SymptomsLog | idx_prediction_id | prediction_id | B-Tree | Prediction detail lookup |
| SymptomsLog | idx_symptom_id | symptom_id | B-Tree | Symptom occurrence analytics |
| SymptomsLog | idx_timestamp | timestamp | B-Tree | Time-based queries |
| DiseaseSymptom | PRIMARY | ds_id | B-Tree | Primary key lookup |
| DiseaseSymptom | idx_disease_symptom | disease_id, symptom_id | B-Tree, UNIQUE | Unique disease-symptom pair |
| DiseaseSymptom | idx_disease_id | disease_id | B-Tree | Disease symptom lookup |
| DiseaseSymptom | idx_symptom_id | symptom_id | B-Tree | Symptom disease lookup |
| DiseaseSymptom | idx_frequency | frequency | B-Tree | Frequency-based analysis |

### 8.5.3 Query Performance Optimization

The following query patterns are optimized through the index design:

**Pattern 1: User Prediction History**
```sql
SELECT * FROM Predictions 
WHERE user_id = ? 
ORDER BY timestamp DESC 
LIMIT 20;
-- Optimized by: idx_user_timestamp (composite index)
```

**Pattern 2: Disease Advice Retrieval**
```sql
SELECT * FROM MedicalAdvice 
WHERE disease_id = ? AND advice_type = ? AND is_active = TRUE 
ORDER BY priority ASC;
-- Optimized by: idx_disease_type (composite index) + idx_priority
```

**Pattern 3: Prediction Analytics**
```sql
SELECT predicted_disease, COUNT(*) as count, AVG(confidence) as avg_confidence
FROM Predictions 
WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY predicted_disease
ORDER BY count DESC;
-- Optimized by: idx_timestamp + idx_predicted_disease
```

**Pattern 4: Symptom Extraction Verification**
```sql
SELECT s.name, sl.matched_variant, sl.severity, sl.extraction_confidence
FROM SymptomsLog sl
JOIN Symptoms s ON sl.symptom_id = s.symptom_id
WHERE sl.prediction_id = ?
ORDER BY sl.extraction_confidence DESC;
-- Optimized by: idx_prediction_id on SymptomsLog + PRIMARY on Symptoms
```

## 8.6 Data Seeding and Initialization

### 8.6.1 Initial Data Population

The database is initialized with seed data for the 30 diseases, 62+ symptoms, and their associations:

```sql
-- Seed: Diseases
INSERT INTO Diseases (name, display_name, severity, description, treatment, precautions, category, body_system) VALUES
('fungal_infection', 'Fungal Infection', 'Mild', 
 'A fungal infection is a skin disease caused by fungi...',
 'Consult a dermatologist. Maintain hygiene. Use antifungal creams.',
 '["bath twice", "use detol or neem in bathing water", "keep infected area dry", "use clean cloths"]',
 'infectious', 'integumentary'),
('allergy', 'Allergy', 'Mild',
 'An allergy is an immune system response to a foreign substance...',
 'Avoid allergens. Take antihistamines. Consult an allergist.',
 '["avoid allergen exposure", "use protective gear", "keep surroundings clean", "consult doctor"]',
 'immunological', 'immune'),
-- ... additional diseases
;

-- Seed: Symptoms
INSERT INTO Symptoms (name, canonical_name, display_name, category, body_system, description, common_variants) VALUES
('fever', 'fever', 'Fever', 'general', 'general', 'Elevated body temperature', '["feverish", "febrile", "high temperature", "pyrexia"]'),
('headache', 'headache', 'Headache', 'neurological', 'nervous', 'Pain in the head or upper neck', '["head pain", "migraine", "tension headache"]'),
('cough', 'cough', 'Cough', 'respiratory', 'respiratory', 'Forceful expulsion of air from the lungs', '["coughing", "hacking", "dry cough", "wet cough"]'),
-- ... additional symptoms
;

-- Seed: Disease-Symptom Associations
INSERT INTO DiseaseSymptom (disease_id, symptom_id, frequency, is_required, is_distinguishing) VALUES
(1, (SELECT symptom_id FROM Symptoms WHERE name = 'itching'), 0.95, TRUE, TRUE),
(1, (SELECT symptom_id FROM Symptoms WHERE name = 'skin_rash'), 0.92, TRUE, TRUE),
(1, (SELECT symptom_id FROM Symptoms WHERE name = 'nodal_skin_eruptions'), 0.78, FALSE, TRUE),
(2, (SELECT symptom_id FROM Symptoms WHERE name = 'continuous_sneezing'), 0.91, TRUE, TRUE),
(2, (SELECT symptom_id FROM Symptoms WHERE name = 'shivering'), 0.85, FALSE, FALSE),
-- ... additional associations
;
```

## 8.7 Backup and Maintenance

### 8.7.1 Backup Strategy

| Backup Type | Frequency | Retention | Method |
|-------------|-----------|-----------|--------|
| Full Database Dump | Daily | 30 days | mysqldump + compression |
| Incremental Binary Log | Continuous | 7 days | MySQL binlog |
| Model Files | On deployment | 10 versions | File system snapshot |
| Disaster Recovery | Weekly | 90 days | Off-site cloud storage |

### 8.7.2 Maintenance Tasks

```sql
-- Weekly: Optimize tables
OPTIMIZE TABLE Predictions, SymptomsLog, DiseaseSymptom;

-- Monthly: Analyze tables for query optimizer
ANALYZE TABLE Users, Diseases, Symptoms, Predictions, MedicalAdvice;

-- Monthly: Archive old predictions (move to archive table)
INSERT INTO Predictions_Archive SELECT * FROM Predictions 
WHERE timestamp < DATE_SUB(NOW(), INTERVAL 1 YEAR);
DELETE FROM Predictions WHERE timestamp < DATE_SUB(NOW(), INTERVAL 1 YEAR);
```

## 8.8 Conclusion

The database design for the Smart Medical Assistant provides a robust, normalized foundation for all data persistence requirements. The schema supports user management, disease reference data, prediction logging, medical advice storage, and detailed symptom extraction tracking. The comprehensive indexing strategy ensures query performance for the most common access patterns, while the foreign key constraints maintain referential integrity across the relational structure.

The design accommodates future growth through its modular structure and extensible JSON columns for semi-structured data. The audit trail provided by the Predictions and SymptomsLog tables supports both user-facing history features and internal model performance monitoring. The junction table pattern (DiseaseSymptom) correctly models the many-to-many relationship between diseases and symptoms, enabling rich analytical queries that can inform continuous model improvement.

The database schema is ready for production deployment, with proper character set configuration (utf8mb4), engine selection (InnoDB for transaction support), and maintenance procedures defined. The seed data scripts provide a complete initialization path for new deployments, ensuring that the system is functional immediately after database creation.
