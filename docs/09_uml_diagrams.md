# Chapter 9: UML Diagrams and System Modeling

## 9.1 Introduction

Unified Modeling Language (UML) diagrams provide a standardized visual representation of system structure, behavior, and interactions. In the context of the Smart Medical Assistant graduation project, UML diagrams serve as critical documentation artifacts that communicate the system's design to technical stakeholders, including reviewers, advisors, and future maintainers. This chapter presents comprehensive text-based UML diagrams covering four essential perspectives: use cases (functional requirements), activities (workflow logic), sequences (temporal interactions), and classes (static structure).

The text-based approach ensures that these diagrams remain readable in plain-text environments, version-controlled documentation, and printed reports without requiring specialized UML rendering tools. Each diagram is presented in ASCII art format with accompanying textual descriptions to ensure clarity and accessibility.

## 9.2 Use Case Diagram

The use case diagram identifies the functional requirements of the Smart Medical Assistant from the perspective of external actors who interact with the system. The diagram captures the primary use cases organized by actor, showing the relationships between actors and system functionality.

### 9.2.1 Use Case Diagram (ASCII)

```
+-----------------------------------------------------------------------------+
|                         USE CASE DIAGRAM                                    |
|                    Smart Medical Assistant System                           |
+-----------------------------------------------------------------------------+

     +-----------+                              +-----------+
     |  PATIENT  |                              |  DOCTOR   |
     |  (Primary |                              |  (Secondary|
     |   Actor)  |                              |   Actor)  |
     +-----+-----+                              +-----+-----+
           |                                          |
           |                                          |
           |      +--------------------------------+  |
           |      |       SYSTEM BOUNDARY          |  |
           |      |                                |  |
           |      |  +------------------------+  |  |
           |      |  | UC1: Describe Symptoms |  |  |
           +------+->|     (Free Text Input)    |  |  |
           |      |  +------------------------+  |  |
           |      |           |                  |  |
           |      |           v                  |  |
           |      |  +------------------------+  |  |
           |      |  | UC2: Select Symptoms  |  |  |
           |      |  |    (From Checklist)    |  |  |
           |      |  +------------------------+  |  |
           |      |           |                  |  |
           |      |           v                  |  |
           |      |  +------------------------+  |  |
           |      |  | UC3: View Analysis    |  |  |
           |      |  |   Results & Prediction |  |  |
           +------+->|                        |  |  |
           |      |  +------------------------+  |  |
           |      |           |                  |  |
           |      |           v                  |  |
           |      |  +------------------------+  |  |
           |      |  | UC4: View Disease     |  |  |
           |      |  |    Information         |  |  |
           +------+->|                        |  |  |
           |      |  +------------------------+  |  |
           |      |           |                  |  |
           |      |           v                  |  |
           |      |  +------------------------+  |  |
           |      |  | UC5: View Treatment   |  |  |
           |      |  |  & Precautions         |  |  |
           +------+->|                        |  |  |
           |      |  +------------------------+  |  |
           |      |           |                  |  |
           |      |           v                  |  |
           |      |  +------------------------+  |  |
           |      |  | UC6: View Prediction  |  |  |
           |      |  |       History          |  |  |
           +------+->|     (Login Required)   |  |  |
           |      |  +------------------------+  |  |
           |      |                                |  |
           |      |  +------------------------+  |  |
           |      |  | UC7: Register Account |  |  |
           +------+->|                        |  |  |
           |      |  +------------------------+  |  |
           |      |           |                  |  |
           |      |           v                  |  |
           |      |  +------------------------+  |  |
           |      |  | UC8: Login / Logout   |  |  |
           +------+->|                        |  |  |
           |      |  +------------------------+  |  |
           |      |                                |  |
           |      |           |                    |  |
           |      |           |                    |  |
           |      |           |  +------------------------+  |
           |      |           |  | UC9: Manage Disease    |  |
           |      |           |  |    Information         |  |
           |      |           +->|     (CRUD)             |  |
           |      |              |  +------------------------+  |
           |      |              |           |                  |
           |      |              |           v                  |
           |      |              |  +------------------------+  |
           |      |              |  | UC10: Manage Symptoms  |  |
           |      |              |  |    Dictionary          |  |
           |      |              +->|     (CRUD)             |  |
           |      |                 |  +------------------------+  |
           |      |                 |           |                  |
           |      |                 |           v                  |
           |      |                 |  +------------------------+  |
           |      |                 |  | UC11: View System      |  |
           |      |                 |  |    Analytics & Logs    |  |
           |      |                 +->|                        |  |
           |      |                    |  +------------------------+  |
           |      |                    |           |                  |
           |      |                    |           v                  |
           |      |                    |  +------------------------+  |
           |      |                    |  | UC12: Manage Users     |  |
           |      |                    |  |    & Permissions     |  |
           |      |                    +->|                        |  |
           |      |                       |  +------------------------+  |
           |      |                       |                            |  |
           |      |                       |                            |  |
           |      |                       |                            |  |
           |      |                       |                            |  |
           |      |  +------------------------+                        |  |
           |      |  | UC13: Provide Feedback |                        |  |
           |      |  |   on Predictions       |                        |  |
           |      |  |   (Login Required)     |                        |  |
           |      |  +------------------------+                        |  |
           |      |                                                     |  |
           |      +--------------------------------+                    |  |
           |                                       |                    |  |
           |                                       |                    |  |
           |                                       |                    |  |
     +-----+-----+                              +----+----+         +----+----+
     |  PATIENT  |                              |  DOCTOR |         |  ADMIN  |
     |           |                              |         |         | (System |
     |           |                              |         |         |  Admin) |
     +-----------+                              +---------+         +---------+


+-----------------------------------------------------------------------------+
| RELATIONSHIP LEGEND                                                         |
|                                                                             |
| Patient ──────> UCx    : Patient initiates or participates in the use case |
| Doctor ───────> UCx    : Doctor initiates or participates in the use case |
| Admin ────────> UCx    : System admin initiates or participates in use case|
| UCx ─────────> UCy     : Include relationship (UCx always includes UCy)     |
| UCx - - - - > UCy     : Extend relationship (UCy optionally extends UCx)  |
+-----------------------------------------------------------------------------+
```

### 9.2.2 Use Case Descriptions

| ID | Use Case | Actor | Description | Priority |
|----|----------|-------|-------------|----------|
| UC1 | Describe Symptoms | Patient | Enter free-text symptom description using natural language | High |
| UC2 | Select Symptoms | Patient | Choose symptoms from a predefined checklist interface | High |
| UC3 | View Analysis Results | Patient | Receive disease prediction with confidence scores | High |
| UC4 | View Disease Information | Patient | Read detailed description of predicted disease | High |
| UC5 | View Treatment & Precautions | Patient | Access recommended treatment and preventive measures | High |
| UC6 | View Prediction History | Patient | Review past symptom analyses and predictions | Medium |
| UC7 | Register Account | Patient | Create a new user account with profile information | Medium |
| UC8 | Login / Logout | Patient | Authenticate to access personalized features | Medium |
| UC9 | Manage Disease Information | Doctor | Create, update, or delete disease reference data | Medium |
| UC10 | Manage Symptoms Dictionary | Doctor | Maintain the canonical symptom vocabulary | Medium |
| UC11 | View System Analytics | Admin | Monitor prediction accuracy, usage statistics, and system health | Low |
| UC12 | Manage Users & Permissions | Admin | Manage user accounts, roles, and access control | Low |
| UC13 | Provide Feedback on Predictions | Patient | Submit accuracy feedback for predictions to improve the model | Medium |

### 9.2.3 Use Case Relationships

**Include Relationships:**
- UC3 (View Analysis Results) includes UC1 (Describe Symptoms) or UC2 (Select Symptoms) — the analysis requires symptom input.
- UC4 (View Disease Information) includes UC3 (View Analysis Results) — disease details are presented as part of the analysis results.
- UC5 (View Treatment & Precautions) includes UC4 (View Disease Information) — treatment and precautions are components of disease information.

**Extend Relationships:**
- UC13 (Provide Feedback) extends UC3 (View Analysis Results) — feedback is an optional action after viewing results.
- UC6 (View Prediction History) extends UC8 (Login) — history viewing requires prior authentication.

## 9.3 Activity Diagram

The activity diagram models the workflow of the primary system process: a patient describing symptoms and receiving a disease prediction. The diagram captures decision points, parallel activities, and the flow of control from start to finish.

### 9.3.1 Activity Diagram: Symptom Analysis Workflow (ASCII)

```
+-----------------------------------------------------------------------------+
|                    ACTIVITY DIAGRAM                                         |
|            Patient Describes Symptoms → System Processes → Results Shown  |
+-----------------------------------------------------------------------------+

                             +----------------+
                             |   [START]      |
                             | Patient opens  |
                             |   web app      |
                             +--------+-------+
                                      |
                                      v
                             +----------------+
                             |  [Activity]    |
                             | Choose input   |
                             | method:        |
                             | Text OR List   |
                             +--------+-------+
                                      |
                                      v
                             +----------------+
                             |  [Decision]    |
                             | Input method?  |
                             +--------+-------+
                                      |
                    +-----------------+-----------------+
                    | Text Input                          | Structured List
                    v                                     v
           +----------------+                      +----------------+
           |  [Activity]    |                      |  [Activity]    |
           | Type symptom   |                      | Select symptoms|
           | description in |                      | from checklist |
           | natural language                      | interface      |
           +--------+-------+                      +--------+-------+
                    |                                       |
                    +-----------------+---------------------+
                                      |
                                      v
                             +----------------+
                             |  [Activity]    |
                             | Submit symptoms|
                             | to API         |
                             +--------+-------+
                                      |
                                      v
                             +----------------+
                             |  [Activity]    |
                             | NLP Engine     |
                             | extracts and   |
                             | normalizes     |
                             | symptoms       |
                             +--------+-------+
                                      |
                                      v
                             +----------------+
                             |  [Decision]    |
                             | Extraction     |
                             | confidence     |
                             | >= 0.4?        |
                             +--------+-------+
                                      |
                    +-----------------+-----------------+
                    | YES                                   | NO
                    v                                     v
           +----------------+                      +----------------+
           |  [Activity]    |                      |  [Activity]    |
           | Build TF-IDF   |                      | Request        |
           | feature vector |                      | clarification  |
           | from symptoms  |                      | from patient   |
           +--------+-------+                      +--------+-------+
                    |                                       |
                    |                                       |
                    v                                       |
           +----------------+                                |
           |  [Activity]    |                                |
           | ML Model       |                                |
           | predicts       |                                |
           | diseases with  |                                |
           | probabilities  |                                |
           +--------+-------+                                |
                    |                                       |
                    |                                       |
                    v                                       |
           +----------------+                                |
           |  [Activity]    |                                |
           | Enrich         |                                |
           | predictions    |                                |
           | with disease   |                                |
           | details from   |                                |
           | database       |                                |
           +--------+-------+                                |
                    |                                       |
                    |                                       |
                    v                                       |
           +----------------+                                |
           |  [Activity]    |                                |
           | Log prediction |                                |
           | and symptoms   |                                |
           | to database    |                                |
           +--------+-------+                                |
                    |                                       |
                    |                                       |
                    v                                       v
           +----------------+                      +----------------+
           |  [Activity]    |                      |  [Activity]    |
           | Display results|                      | Return to    |
           | with disease,  |                      | input form   |
           | confidence,    |                      | with guidance|
           | treatment,     |                      |              |
           | precautions  |                      |              |
           +--------+-------+                      +--------+-------+
                    |                                       |
                    |                                       |
                    v                                       v
           +----------------+                      +----------------+
           |  [Decision]    |                      |  [Activity]    |
           | User logged    |<---------------------| Patient enters |
           | in?            |                      | more symptoms  |
           +--------+-------+                      +----------------+
                    |
          +---------+---------+
          | YES                 | NO
          v                     v
  +----------------+    +----------------+
  |  [Activity]    |    |  [Activity]    |
  | Save to user's |    | Show login     |
  | prediction     |    | prompt for     |
  | history        |    | history saving |
  +--------+-------+    +--------+-------+
           |                     |
           |                     |
           v                     v
  +----------------+    +----------------+
  |  [Decision]    |    |  [Decision]    |
  | Provide        |    | Continue       |
  | feedback?      |    | without saving?|
  +--------+-------+    +--------+-------+
           |                     |
    +------+------+        +------+------+
    | YES         | NO     | YES         | NO
    v             v        v             v
  +----------------+   +----------------+
  |  [Activity]    |   |  [Activity]    |
  | Collect user   |   | Return to      |
  | feedback on    |   | main page      |
  | prediction     |   |                |
  | accuracy       |   |                |
  +--------+-------+   +--------+-------+
           |                     |
           |                     |
           v                     v
           +----------------+
           |     [END]      |
           | Patient exits  |
           | or starts new  |
           | analysis       |
           +----------------+

+-----------------------------------------------------------------------------+
| ACTIVITY LEGEND                                                             |
|                                                                             |
| [START] / [END]    : Initial and final nodes                               |
| [Activity]         : Action or process to be performed                        |
| [Decision]         : Branching condition with yes/no or multiple paths      |
| |                  : Control flow (solid line)                                |
| |                  | : Control flow (solid line)                            |
| +-----------------+ : Merge of multiple paths                                |
| +----------------> : Join/merge point                                       |
+-----------------------------------------------------------------------------+
```

### 9.3.2 Activity Description: Symptom Analysis Workflow

| Step | Activity | Actor/System | Description | Decision Criteria |
|------|----------|-------------|-------------|-------------------|
| 1 | Start | Patient | Patient opens the Smart Medical Assistant web application | — |
| 2 | Choose Input Method | Patient | Patient selects between free-text input or structured symptom checklist | Input preference |
| 3 | Text Input | Patient | Patient types a natural language description of their symptoms | — |
| 4 | Structured Selection | Patient | Patient selects symptoms from a predefined checklist with categories | — |
| 5 | Submit to API | Frontend | Frontend sends the symptom data to the Flask backend API | — |
| 6 | NLP Extraction | System | NLP engine parses and extracts canonical symptoms from the input | — |
| 7 | Confidence Check | System | System evaluates whether extracted symptoms are sufficient for reliable prediction | Confidence >= 0.4? |
| 8 | Request Clarification | System | If confidence is too low, system asks patient for more specific symptoms | — |
| 9 | Build Feature Vector | System | System constructs a TF-IDF feature vector from the canonical symptom list | — |
| 10 | ML Prediction | System | XGBoost model predicts disease probabilities from the feature vector | — |
| 11 | Enrich Predictions | System | System queries the database for disease descriptions, treatments, and precautions | — |
| 12 | Log Prediction | System | System saves the prediction request, symptoms, and results to the database | — |
| 13 | Display Results | System | Frontend renders the prediction results with disease cards, confidence scores, and advice | — |
| 14 | Check Authentication | System | System checks if the patient is logged in for history saving | Logged in? |
| 15 | Save to History | System | If authenticated, the prediction is saved to the user's history | — |
| 16 | Show Login Prompt | System | If not authenticated, system offers login to save history | — |
| 17 | Feedback Decision | Patient | Patient decides whether to provide accuracy feedback on the prediction | Provide feedback? |
| 18 | Collect Feedback | Patient | Patient submits feedback (accurate, inaccurate, uncertain) with optional notes | — |
| 19 | End | Patient | Patient exits or starts a new symptom analysis | — |

## 9.4 Sequence Diagram

The sequence diagram illustrates the temporal order of interactions between system components during a typical symptom analysis request. It shows the messages exchanged between the User, Frontend, API, NLP Engine, ML Predictor, and Database, along with the lifelines of each component.

### 9.4.1 Sequence Diagram: Symptom Analysis Request (ASCII)

```
+-----------------------------------------------------------------------------+
|                         SEQUENCE DIAGRAM                                    |
|       User → Frontend → API → NLP → ML → Database → Response               |
+-----------------------------------------------------------------------------+

     User        Frontend        API          NLP         ML       Database
      |             |              |            |           |            |
      |             |              |            |           |            |
      | (1) Enter symptom        |            |           |            |
      |     description            |            |           |            |
      |------------>|              |            |           |            |
      |             |              |            |           |            |
      |             | (2) Click "Analyze"     |           |            |
      |             |     button               |           |            |
      |             |------------>|            |           |            |
      |             |              |            |           |            |
      |             | (3) POST /api/analyze    |           |            |
      |             |     {description: ...}   |           |            |
      |             |------------>|            |           |            |
      |             |              |            |           |            |
      |             |              | (4) Validate input     |            |
      |             |              |     & check rate      |            |
      |             |              |     limit             |            |
      |             |              |<-----------|           |            |
      |             |              |            |           |            |
      |             |              | (5) extract_symptoms()   |            |
      |             |              |---------->|            |            |
      |             |              |            |           |            |
      |             |              |            | (6) Tokenize &        |
      |             |              |            |     normalize text    |
      |             |              |            |<-----------|            |
      |             |              |            |           |            |
      |             |              |            | (7) Pattern match     |
      |             |              |            |     against dictionary  |
      |             |              |            |<-----------|            |
      |             |              |            |           |            |
      |             |              |            | (8) Detect negation,   |
      |             |              |            |     severity, duration |
      |             |              |            |<-----------|            |
      |             |              |            |           |            |
      |             |              | (9) Return extracted  |            |
      |             |              |     symptoms + conf   |            |
      |             |              |<-----------|           |            |
      |             |              |            |           |            |
      |             |              | (10) Check confidence  |            |
      |             |              |     >= 0.4?             |            |
      |             |              |            |           |            |
      |             |              | (11) Build TF-IDF     |            |
      |             |              |     feature vector    |            |
      |             |              |------------------------>|            |
      |             |              |            |           |            |
      |             |              |            | (12) predict_proba()  |
      |             |              |            |           |            |
      |             |              |            | (13) Load XGBoost     |
      |             |              |            |     model from disk   |
      |             |              |            |<----------------------|
      |             |              |            |           |            |
      |             |              |            | (14) Compute disease  |
      |             |              |            |     probabilities     |
      |             |              |            |<-----------|            |
      |             |              |            |           |            |
      |             |              | (15) Return top-k     |            |
      |             |              |     predictions       |            |
      |             |              |<------------------------|            |
      |             |              |            |           |            |
      |             |              | (16) Query disease     |            |
      |             |              |     details (treatment,|            |
      |             |              |     precautions)      |            |
      |             |              |------------------------------------>|
      |             |              |            |           |            |
      |             |              |            |           | (17) SELECT |
      |             |              |            |           |     FROM    |
      |             |              |            |           |     Diseases|
      |             |              |            |           |     JOIN    |
      |             |              |            |           |     Medical |
      |             |              |            |           |     Advice  |
      |             |              |            |           |<-----------|
      |             |              |            |           |            |
      |             |              | (18) Return disease   |            |
      |             |              |     information records            |            |
      |             |              |<------------------------------------|            |
      |             |              |            |           |            |
      |             |              | (19) Assemble JSON    |            |
      |             |              |     response with     |            |
      |             |              |     predictions +     |            |
      |             |              |     disease details   |            |
      |             |              |            |           |            |
      |             |              | (20) Log prediction   |            |
      |             |              |     to database       |            |
      |             |              |------------------------------------>|
      |             |              |            |           |            |
      |             |              |            |           | (21) INSERT|
      |             |              |            |           |     INTO   |
      |             |              |            |           |     Predict |
      |             |              |            |           |     ions    |
      |             |              |            |           |<-----------|
      |             |              |            |           |            |
      |             | (22) Return JSON        |            |           |            |
      |             |     response            |            |           |            |
      |             |<------------------------|            |           |            |
      |             |              |            |           |            |
      | (23) Render results       |            |            |           |            |
      |     cards with disease,   |            |            |           |            |
      |     confidence, treatment|            |            |           |            |
      |<------------|              |            |           |            |
      |             |              |            |           |            |
      |             |              |            |           |            |
      | (24) User reads results   |            |            |           |            |
      |     and optionally        |            |            |           |            |
      |     provides feedback     |            |            |           |            |
      |------------>|              |            |           |            |
      |             |              |            |           |            |
      |             | (25) POST /api/feedback  |            |           |            |
      |             |------------>|            |           |            |
      |             |              |            |           |            |
      |             |              | (26) Update prediction|            |            |
      |             |              |     with user feedback|            |            |
      |             |              |------------------------------------>|
      |             |              |            |           |            |
      |             |              |            |           | (27) UPDATE|
      |             |              |            |           |     Predict |
      |             |              |            |           |     ions SET|
      |             |              |            |           |     feedback|
      |             |              |            |           |<-----------|
      |             |              |            |           |            |
      |             |              | (28) Return success   |            |            |
      |             |<-------------|            |           |            |
      |             |              |            |           |            |
      | (29) Display              |            |            |           |            |
      |     confirmation          |            |            |           |            |
      |<------------|              |            |           |            |
      |             |              |            |           |            |

+-----------------------------------------------------------------------------+
| SEQUENCE LEGEND                                                             |
|                                                                             |
| --->  : Synchronous message call (request)                                 |
| -->>  : Return message (response)                                          |
| |     : Lifeline (dashed line shows component is active)                   |
| |     |                                                                    |
| +---| : Activation bar (solid rectangle shows component is processing)    |
+-----------------------------------------------------------------------------+
```

### 9.4.2 Sequence Description

| Step | From | To | Message | Data | Description |
|------|------|----|---------|------|-------------|
| 1 | User | Frontend | Enter symptom description | Natural language text | User describes symptoms in the input form |
| 2 | User | Frontend | Click "Analyze" | UI event | User triggers the analysis request |
| 3 | Frontend | API | POST /api/analyze | JSON payload with description | Frontend sends the symptom description to the API |
| 4 | API | API | Validate & rate limit | Internal check | API validates input and checks rate limits |
| 5 | API | NLP | extract_symptoms() | Description text | API delegates symptom extraction to NLP engine |
| 6-8 | NLP | NLP | Internal processing | — | NLP engine tokenizes, normalizes, pattern matches, and detects attributes |
| 9 | NLP | API | Return extracted symptoms | Structured symptom list | NLP returns canonical symptoms with metadata |
| 10 | API | API | Confidence check | Confidence score | API verifies extraction confidence is sufficient |
| 11 | API | ML | Build TF-IDF vector | Symptom list | API constructs feature vector for ML model |
| 12-14 | ML | ML | Internal prediction | Feature vector | ML model loads and computes disease probabilities |
| 15 | ML | API | Return top-k predictions | Probability distribution | ML returns ranked disease predictions |
| 16-18 | API | Database | Query disease details | Disease IDs | API retrieves treatment, precautions, and descriptions |
| 19 | API | API | Assemble JSON response | All data | API compiles the complete response payload |
| 20-21 | API | Database | Log prediction | Prediction data | API saves the prediction to the audit log |
| 22 | API | Frontend | Return JSON response | Complete response | API sends the final response to the frontend |
| 23 | Frontend | User | Render results | HTML/JS | Frontend displays disease prediction cards |
| 24 | User | Frontend | Provide feedback | Feedback selection | User optionally submits accuracy feedback |
| 25-28 | Frontend | API | POST /api/feedback | Feedback data | Frontend sends feedback to the API |
| 29 | Frontend | User | Display confirmation | UI update | Frontend confirms feedback receipt |

## 9.5 Class Diagram

The class diagram defines the static structure of the Smart Medical Assistant system, showing all major classes, their attributes, methods, and relationships. The diagram captures the object-oriented design of the Python backend, including the Flask application layer, NLP subsystem, ML pipeline, and data access layer.

### 9.5.1 Class Diagram (ASCII)

```
+-----------------------------------------------------------------------------+
|                           CLASS DIAGRAM                                     |
|                    Smart Medical Assistant System                           |
+-----------------------------------------------------------------------------+

+------------------------+        +------------------------+        +------------------------+
|     FlaskApp           |<>-----|    ConfigManager       |        |    CORSManager         |
+------------------------+        +------------------------+        +------------------------+
| - app: Flask           |        | - config: dict         |        | - origins: list        |
| - db: SQLAlchemy       |        | - env: str             |        | - methods: list        |
| - model: XGBClassifier |        | - debug: bool          |        | - headers: list        |
+------------------------+        +------------------------+        +------------------------+
| + __init__()           |        | + load_config()        |        | + init_app()           |
| + register_blueprints()|        | + get_db_uri()         |        | + handle_preflight()   |
| + register_error_handlers()    | + get_model_path()     |        | + apply_headers()      |
| + run()                |        | + is_production()      |        +------------------------+
| + create_app()         |        +------------------------+
+------------------------+                   |
          |                                  |
          | uses                             | uses
          |                                  |
          v                                  v
+------------------------+        +------------------------+
|     APIRoutes          |        |    DatabaseManager     |
+------------------------+        +------------------------+
| - symptom_analyzer:   |        | - engine: Engine       |
|   SymptomAnalyzer      |        | - session: Session     |
| - auth_service:        |        | - connection_pool: Pool|
|   AuthService          |        +------------------------+
+------------------------+        | + connect()            |
| + health_check()       |        | + disconnect()       |
| + analyze_symptoms()   |        | + execute_query()      |
| + predict_disease()    |        | + begin_transaction()  |
| + get_diseases()       |        | + commit()             |
| + get_symptoms()       |        | + rollback()           |
| + register_user()      |        | + get_session()        |
| + login_user()         |        +------------------------+
| + logout_user()        |                   |
| + submit_feedback()     |                   | manages
+------------------------+                   |
          |                                  v
          | uses                    +------------------------+
          |                         |      UserModel         |
          |                         +------------------------+
          |                         | - user_id: int         |
          |                         | - username: str        |
          |                         | - email: str           |
          |                         | - password_hash: str   |
          |                         | - full_name: str       |
          |                         | - age: int             |
          |                         | - gender: str          |
          |                         | - created_at: datetime |
          |                         | - is_active: bool      |
          |                         +------------------------+
          |                         | + create()             |
          |                         | + authenticate()       |
          |                         | + update_profile()     |
          |                         | + deactivate()         |
          |                         | + get_history()        |
          |                         +------------------------+
          |                                    |
          |                                    | 1:N
          |                                    v
          |                         +------------------------+
          |                         |   PredictionModel      |
          |                         +------------------------+
          |                         | - prediction_id: int   |
          |                         | - user_id: int         |
          |                         | - input_text: str      |
          |                         | - predicted_disease: str|
          |                         | - confidence: float     |
          |                         | - nlp_confidence: float|
          |                         | - top_3_results: JSON |
          |                         | - model_version: str  |
          |                         | - processing_time_ms: int|
          |                         | - user_feedback: str  |
          |                         | - timestamp: datetime |
          |                         | - ip_address: str     |
          |                         +------------------------+
          |                         | + create()             |
          |                         | + get_by_user()        |
          |                         | + get_by_disease()     |
          |                         | + add_feedback()       |
          |                         | + get_stats()          |
          |                         +------------------------+
          |                                    |
          | uses                               | 1:N
          |                                    v
          |                         +------------------------+
          |                         |   SymptomsLogModel       |
          |                         +------------------------+
          |                         | - log_id: int          |
          |                         | - prediction_id: int   |
          |                         | - symptom_id: int      |
          |                         | - matched_variant: str |
          |                         | - severity: str        |
          |                         | - duration: str        |
          |                         | - is_negated: bool     |
          |                         | - extraction_confidence: float|
          |                         +------------------------+
          |                         | + create()             |
          |                         | + get_by_prediction()    |
          |                         | + get_symptom_stats()  |
          |                         +------------------------+
          |
          | uses
          v
+------------------------+        +------------------------+        +------------------------+
|    SymptomAnalyzer     |<>-----|     NLPEngine          |<>-----|   SymptomDictionary    |
+------------------------+        +------------------------+        +------------------------+
| - nlp_engine: NLPEngine|        | - tokenizer: Tokenizer |        | - symptom_map: dict    |
| - symptom_dict:        |        | - normalizer: Normalizer|       | - canonical_names: list|
|   SymptomDictionary    |        | - extractor:           |        | - variant_map: dict    |
| - tfidf_vectorizer:    |        |   SymptomExtractor     |        | - categories: dict     |
|   TfidfVectorizer      |        | - severity_detector:   |        | - body_systems: dict   |
| - model: XGBClassifier |        |   SeverityDetector     |        +------------------------+
| - label_encoder:       |        | - duration_detector:   |        | + load_from_file()     |
|   LabelEncoder         |        |   DurationDetector     |        | + get_canonical()      |
| - disease_db:          |        | - confidence_scorer:   |        | + get_variants()       |
|   DiseaseRepository    |        |   ConfidenceScorer     |        | + get_category()       |
+------------------------+        +------------------------+        | + search()             |
| + analyze_description()|        | + process_text()       |        | + add_symptom()        |
| + analyze_symptom_list()|       | + extract_symptoms()   |        | + update_symptom()     |
| + predict_from_vector()|        | + detect_severity()    |        +------------------------+
| + enrich_prediction()  |        | + detect_duration()    |
| + log_prediction()     |        | + score_confidence()   |
+------------------------+        | + get_recommendation() |
          |                       +------------------------+
          | uses
          v
+------------------------+        +------------------------+
|    MLModelManager      |<>-----|    ModelPersistence    |
+------------------------+        +------------------------+
| - model: XGBClassifier |        | - model_path: str      |
| - vectorizer:          |        | - vectorizer_path: str |
|   TfidfVectorizer      |        | - encoder_path: str    |
| - label_encoder:       |        | - preprocessor_path: str|
|   LabelEncoder         |        +------------------------+
| - preprocessor:        |        | + save_model()         |
|   DataPreprocessor     |        | + load_model()         |
+------------------------+        | + save_vectorizer()    |
| + load_model()         |        | + load_vectorizer()    |
| + predict_proba()      |        | + save_encoder()       |
| + get_feature_importance()      | + load_encoder()       |
| + get_top_predictions()|        | + save_preprocessor()  |
| + get_model_info()     |        | + load_preprocessor()  |
+------------------------+        +------------------------+
          |
          | uses
          v
+------------------------+        +------------------------+
|   DiseaseRepository    |<>-----|    DatabaseManager     |
+------------------------+        +------------------------+
| - db: DatabaseManager  |        | (defined above)        |
+------------------------+        +------------------------+
| + get_by_name()        |
| + get_by_id()          |
| + get_all()            |
| + get_by_severity()    |
| + get_by_category()    |
| + get_advice()         |
| + get_symptoms()       |
+------------------------+

+------------------------+        +------------------------+
|    AuthService         |<>-----|    PasswordHasher      |
+------------------------+        +------------------------+
| - db: DatabaseManager  |        | - method: str          |
| - hasher: PasswordHasher|       | - rounds: int          |
| - token_manager:       |        +------------------------+
|   TokenManager         |        | + hash_password()      |
+------------------------+        | + verify_password()      |
| + register()           |        | + generate_salt()      |
| + login()              |        | + check_password()       |
| + logout()             |        +------------------------+
| + verify_token()       |
| + refresh_token()      |
| + reset_password()     |
+------------------------+
          |
          | uses
          v
+------------------------+
|    TokenManager        |
+------------------------+
| - secret_key: str      |
| - algorithm: str       |
| - expires_in: int      |
+------------------------+
| + generate_token()     |
| + verify_token()       |
| + decode_token()       |
| + get_expiry()         |
+------------------------+

+-----------------------------------------------------------------------------+
| CLASS RELATIONSHIP LEGEND                                                   |
|                                                                             |
| ----|>        : Association (one class uses another)                         |
| ----<>-----   : Aggregation (whole-part relationship, part can exist alone)|
| ----<>>----   : Composition (whole-part relationship, part cannot exist   |
|                 independently of the whole)                                  |
| -------|>     : Inheritance (is-a relationship)                           |
| - attribute   : Private attribute                                           |
| + method()    : Public method                                               |
+-----------------------------------------------------------------------------+
```

### 9.5.2 Class Descriptions

#### FlaskApp

The main application class that initializes the Flask web server, registers API routes, configures middleware, and manages the application lifecycle.

| Attribute | Type | Description |
|-----------|------|-------------|
| app | Flask | The Flask application instance |
| db | SQLAlchemy | SQLAlchemy ORM instance for database operations |
| model | XGBClassifier | Loaded XGBoost classification model |

| Method | Return Type | Description |
|--------|-------------|-------------|
| __init__() | FlaskApp | Constructor; initializes Flask app and extensions |
| register_blueprints() | void | Registers API route blueprints |
| register_error_handlers() | void | Registers global error handler functions |
| run() | void | Starts the development server |
| create_app() | Flask | Factory method; creates and configures the app |

#### SymptomAnalyzer

The central orchestrator class that coordinates the NLP extraction, ML prediction, and result enrichment workflow. It is the primary interface between the API routes and the internal processing components.

| Attribute | Type | Description |
|-----------|------|-------------|
| nlp_engine | NLPEngine | Symptom extraction and attribute detection engine |
| symptom_dict | SymptomDictionary | Canonical symptom vocabulary reference |
| tfidf_vectorizer | TfidfVectorizer | Trained TF-IDF feature vectorizer |
| model | XGBClassifier | Trained disease classification model |
| label_encoder | LabelEncoder | Disease label encoder for class decoding |
| disease_db | DiseaseRepository | Database access layer for disease information |

| Method | Return Type | Description |
|--------|-------------|-------------|
| analyze_description(text) | dict | Full pipeline: extract symptoms, predict, enrich, return results |
| analyze_symptom_list(symptoms) | dict | Predict from pre-selected symptom list (skips NLP) |
| predict_from_vector(vector) | array | Direct prediction from TF-IDF feature vector |
| enrich_prediction(predictions) | list | Enrich predictions with disease details from database |
| log_prediction(data) | int | Save prediction to audit log and return prediction ID |

#### NLPEngine

The natural language processing engine that extracts structured symptom information from free-text user input.

| Attribute | Type | Description |
|-----------|------|-------------|
| tokenizer | Tokenizer | Text tokenization component |
| normalizer | Normalizer | Text normalization component |
| extractor | SymptomExtractor | Symptom dictionary matching component |
| severity_detector | SeverityDetector | Severity qualifier detection component |
| duration_detector | DurationDetector | Temporal expression detection component |
| confidence_scorer | ConfidenceScorer | Extraction confidence scoring component |

| Method | Return Type | Description |
|--------|-------------|-------------|
| process_text(text) | dict | Complete NLP pipeline: normalize, extract, score |
| extract_symptoms(text) | list | Extract canonical symptoms from text |
| detect_severity(text, position) | str | Detect severity modifier for symptom at position |
| detect_duration(text, position) | str | Detect duration expression for symptom at position |
| score_confidence(symptoms, text) | dict | Calculate overall extraction confidence |
| get_recommendation(confidence) | str | Generate user-facing recommendation message |

#### MLModelManager

Manages the loading, inference, and metadata access for the trained machine learning model.

| Attribute | Type | Description |
|-----------|------|-------------|
| model | XGBClassifier | The trained XGBoost classification model |
| vectorizer | TfidfVectorizer | The trained TF-IDF vectorizer |
| label_encoder | LabelEncoder | The fitted label encoder |
| preprocessor | DataPreprocessor | The data preprocessing pipeline |

| Method | Return Type | Description |
|--------|-------------|-------------|
| load_model(path) | void | Load model, vectorizer, and encoder from disk |
| predict_proba(vector) | array | Predict disease probability distribution |
| get_feature_importance() | dict | Return feature importance scores from model |
| get_top_predictions(probabilities, k) | list | Return top-k predictions with disease names |
| get_model_info() | dict | Return model metadata (accuracy, version, classes) |

#### DiseaseRepository

Database access object for disease-related queries, providing an abstraction layer between the business logic and the database schema.

| Attribute | Type | Description |
|-----------|------|-------------|
| db | DatabaseManager | Database connection manager |

| Method | Return Type | Description |
|--------|-------------|-------------|
| get_by_name(name) | dict | Retrieve disease record by name |
| get_by_id(disease_id) | dict | Retrieve disease record by ID |
| get_all() | list | Retrieve all diseases with details |
| get_by_severity(severity) | list | Filter diseases by severity level |
| get_by_category(category) | list | Filter diseases by category |
| get_advice(disease_id) | list | Retrieve medical advice for a disease |
| get_symptoms(disease_id) | list | Retrieve associated symptoms for a disease |

#### AuthService

Handles user authentication, registration, session management, and password security.

| Attribute | Type | Description |
|-----------|------|-------------|
| db | DatabaseManager | Database connection manager |
| hasher | PasswordHasher | Password hashing and verification utility |
| token_manager | TokenManager | JWT or session token management |

| Method | Return Type | Description |
|--------|-------------|-------------|
| register(username, email, password) | dict | Create new user account |
| login(email, password) | dict | Authenticate user and return session token |
| logout(token) | void | Invalidate user session |
| verify_token(token) | dict | Verify session token validity |
| refresh_token(token) | str | Generate new session token from valid token |
| reset_password(email) | void | Initiate password reset workflow |

## 9.6 State Diagram

The state diagram models the lifecycle of a prediction request as it transitions through various states within the system.

### 9.6.1 Prediction Request State Diagram (ASCII)

```
+-----------------------------------------------------------------------------+
|                         STATE DIAGRAM                                       |
|              Prediction Request Lifecycle                                   |
+-----------------------------------------------------------------------------+

                           +-------------+
                           |   [INITIAL] |
                           |   Request   |
                           |   Received  |
                           +------+------+
                                  |
                                  | validate_input()
                                  v
                           +-------------+
                    +----->|  VALIDATING |
                    |      |   Input     |
                    |      +------+------+
                    |             |
                    |   invalid   | valid
                    |             v
                    |      +-------------+
                    |      |  EXTRACTING |
                    |      |  Symptoms   |
                    |      +------+------+
                    |             |
                    |   low_conf  | sufficient
                    |             v
                    |      +-------------+
                    +------|  CLARIFYING |
                    |      |   Needed    |
                    |      +-------------+
                    |             |
                    |             | input_received
                    |             v
                    |      +-------------+
                    |      |  EXTRACTING |
                    |      |  Symptoms   |
                    |      +------+------+
                    |             |
                    +-------------+
                                  |
                                  | symptoms_extracted
                                  v
                           +-------------+
                           |  PREDICTING |
                           |   Disease   |
                           +------+------+
                                  |
                                  | prediction_complete
                                  v
                           +-------------+
                           |  ENRICHING  |
                           |   Results   |
                           +------+------+
                                  |
                                  | data_enriched
                                  v
                           +-------------+
                           |  LOGGING    |
                           |   Request   |
                           +------+------+
                                  |
                                  | logged
                                  v
                           +-------------+
                           |  RESPONDING |
                           |   Client    |
                           +------+------+
                                  |
                                  | response_sent
                                  v
                           +-------------+
                           |  [FINAL]    |
                           |   Complete  |
                           +-------------+

                           +-------------+
                           |   [ERROR]   |
                           |   Failed    |
                           +-------------+
                                  ^
                                  |
                    +-------------+-------------+
                    |                           |
                    | error_occurred            | error_occurred
                    |                           |
                    +---------------------------+

+-----------------------------------------------------------------------------+
| STATE TRANSITION TABLE                                                      |
|                                                                             |
| Current State    | Event               | Next State        | Action        |
|------------------|---------------------|-------------------|---------------|
| INITIAL          | validate_input()    | VALIDATING        | Parse request |
| VALIDATING       | invalid             | CLARIFYING        | Return error  |
| VALIDATING       | valid               | EXTRACTING        | Start NLP     |
| EXTRACTING       | low_confidence      | CLARIFYING        | Request more  |
| EXTRACTING       | sufficient          | PREDICTING        | Build vector  |
| CLARIFYING       | input_received      | EXTRACTING        | Re-extract    |
| PREDICTING       | prediction_complete | ENRICHING        | Query DB      |
| ENRICHING        | data_enriched       | LOGGING          | Format data   |
| LOGGING          | logged              | RESPONDING        | Send response |
| RESPONDING       | response_sent       | FINAL             | Clean up      |
| (Any)            | error_occurred      | ERROR            | Log error     |
+-----------------------------------------------------------------------------+
```

## 9.7 Conclusion

The UML diagrams presented in this chapter provide a comprehensive, multi-perspective view of the Smart Medical Assistant system design. The use case diagram captures the functional requirements from the perspective of three distinct actors (Patient, Doctor, and System Admin), establishing a clear boundary between user-facing functionality and administrative capabilities. The activity diagram traces the complete workflow from symptom input through prediction output, highlighting decision points and alternative paths that the system must handle. The sequence diagram provides a precise, time-ordered view of the inter-component communication during a typical prediction request, serving as an implementation guide for developers integrating the frontend, backend, NLP, and ML components. The class diagram defines the static object-oriented structure of the system, showing the responsibilities, relationships, and interfaces of each major class in the Python backend.

Together, these UML artifacts form a complete design specification that bridges the gap between high-level requirements and low-level implementation. They ensure that all stakeholders — from graduation project advisors to future maintainers — have a clear, consistent understanding of the system's architecture, behavior, and structure. The text-based format ensures accessibility and version control compatibility, making these diagrams living documents that can be updated as the system evolves.
