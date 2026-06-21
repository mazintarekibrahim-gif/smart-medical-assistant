# Installation Guide

This document provides a comprehensive, step-by-step guide to setting up the Smart Medical Assistant project on your local machine or development server.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Step-by-Step Setup](#step-by-step-setup)
- [Virtual Environment](#virtual-environment)
- [Installing Dependencies](#installing-dependencies)
- [Database Setup](#database-setup)
- [Running the Preprocessing Pipeline](#running-the-preprocessing-pipeline)
- [Training the Models](#training-the-models)
- [Starting the Flask API](#starting-the-flask-api)
- [Starting the Frontend](#starting-the-frontend)
- [Troubleshooting](#troubleshooting)
- [Environment Variables](#environment-variables)

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

| Requirement | Minimum Version | Notes |
|-------------|-----------------|-------|
| **Python** | 3.8+ | Recommended: 3.10 or 3.11 |
| **Git** | 2.30+ | For cloning the repository |
| **MySQL** | 5.7+ | Optional; required only if using the database persistence layer |
| **Node.js** | 16+ | Optional; required only if running the frontend |
| **pip** | 21.0+ | Usually bundled with Python |

### Verify Your Environment

```bash
python --version   # Should print 3.8.x or higher
pip --version
mysql --version    # Optional
git --version
node --version     # Optional
```

---

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/smart-medical-assistant.git
cd smart-medical-assistant
```

If you are working with the existing local copy, ensure you are in the project root:

```bash
cd smart-medical-assistant
```

### 2. Checkout the Correct Branch (if applicable)

```bash
git checkout agent/testing
```

---

## Virtual Environment

It is **strongly recommended** to use a virtual environment to avoid dependency conflicts.

### Create the Environment

**Linux / macOS:**

```bash
python -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**

```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

> If you see an execution policy error in PowerShell, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` and try again.

### Verify Activation

Your terminal prompt should now show `(venv)` at the beginning:

```bash
(venv) user@machine:~/smart-medical-assistant$
```

---

## Installing Dependencies

With the virtual environment activated, install all required Python packages:

```bash
pip install -r requirements.txt
```

This may take 2–5 minutes depending on your internet connection and machine performance. The command installs:

- **Web Framework:** Flask, Flask-CORS, FastAPI (optional), Uvicorn (optional)
- **Data Science:** NumPy, Pandas, Scikit-learn, SciPy
- **ML Models:** XGBoost
- **NLP:** NLTK
- **Visualization:** Matplotlib, Seaborn
- **Testing:** pytest, pytest-cov
- **HTTP Client:** requests
- **Deployment:** gunicorn
- **Database:** mysql-connector-python

### NLTK Data Download

The preprocessing and NLP scripts automatically download required NLTK data (`punkt`, `stopwords`, `wordnet`, `omw-1.4`) on first run. If you prefer to download manually:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
```

---

## Database Setup

> **Note:** This step is optional. The API can run in demo mode without a database. MySQL is only needed if you plan to persist user queries, predictions, or feedback.

### 1. Install MySQL

**Ubuntu / Debian:**

```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation
```

**Windows:**

Download and install MySQL Community Server from [https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/).

**macOS (Homebrew):**

```bash
brew install mysql
brew services start mysql
```

### 2. Create the Database and User

Log into MySQL as root:

```bash
mysql -u root -p
```

Execute the following SQL commands:

```sql
-- Create the application database
CREATE DATABASE IF NOT EXISTS smart_medical_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Create a dedicated user (update password as needed)
CREATE USER IF NOT EXISTS 'sma_user'@'localhost' IDENTIFIED BY 'YourSecurePassword123!';

-- Grant privileges
GRANT ALL PRIVILEGES ON smart_medical_db.* TO 'sma_user'@'localhost';
FLUSH PRIVILEGES;

-- Verify
SHOW DATABASES;
EXIT;
```

### 3. Create Tables (if applicable)

If the project includes a schema file, run:

```bash
mysql -u sma_user -p smart_medical_db < schema.sql
```

Otherwise, the application may create tables automatically on first run (check `src/api/app.py` for any `CREATE TABLE` logic).

### 4. Update Environment Variables

Add the following to your `.env` file or environment:

```bash
DB_HOST=localhost
DB_PORT=3306
DB_NAME=smart_medical_db
DB_USER=sma_user
DB_PASSWORD=YourSecurePassword123!
```

---

## Running the Preprocessing Pipeline

The preprocessing pipeline cleans the raw dataset, encodes labels, and prepares TF-IDF features.

```bash
python -c "from src.utils.preprocessing import main; import os; main({'runDir': os.getcwd()})"
```

Or, if you have a dedicated script:

```bash
python -m src.utils.preprocessing
```

### Expected Output

```
Loaded 1357 records from raw dataset
Preprocessor saved to models/preprocessor.pkl

Preprocessing Complete!
Original features: 6
Processed records: 1357
TF-IDF features: ~1800
Disease classes: 30
Saved to: data/processed
```

### Verify Output Files

After running, you should see:

```
data/processed/
  ├── medical_dataset_processed.csv
  ├── tfidf_features.csv
  └── feature_names.txt
models/
  └── preprocessor.pkl
```

---

## Training the Models

Train all ML models and generate comparison reports:

```bash
python -c "from src.ml.train_models import main; import os; main({'runDir': os.getcwd()})"
```

Or:

```bash
python -m src.ml.train_models
```

### Expected Output

```
Training samples: 1085
Testing samples: 272
Features: 1802
Classes: 30

============================================================
Training Logistic Regression...
============================================================
Best Parameters: {'C': 10, 'max_iter': 1000, 'penalty': 'l2', 'solver': 'lbfgs'}
Best CV Score: 0.8234
Accuracy:  0.8456
Precision: 0.8523
Recall:    0.8456
F1 Score:  0.8412
...
Best Model: RandomForest
Best Model saved to: models/best_model.pkl
```

### Verify Model Artifacts

```
models/
  ├── best_model.pkl
  ├── scaler.pkl
  └── preprocessor.pkl
reports/
  ├── model_comparison.csv
  ├── model_comparison.png
  ├── confusion_matrix_RandomForest.png
  └── model_results.json
```

---

## Starting the Flask API

With models trained, start the REST API:

```bash
python -m src.api.app
```

### Expected Output

```
Starting Smart Medical Assistant API...
Model directory: C:\...\smart-medical-assistant\models
Data directory: C:\...\smart-medical-assistant\data\raw
Models loaded: True
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.100:5000
```

### Test the API

```bash
curl http://localhost:5000/api/health
```

Expected response:

```json
{"status": "healthy", "timestamp": "2024-06-21T14:30:00", "models_loaded": true}
```

---

## Starting the Frontend

If your project includes a frontend (e.g., React, Vue, or plain HTML/JS):

```bash
cd frontend
npm install
npm start
```

The frontend typically runs on `http://localhost:3000` and proxies API requests to `http://localhost:5000`.

> Ensure the frontend's API base URL points to the correct backend address. Update `REACT_APP_API_URL` or equivalent in your `.env` file if needed.

---

## Troubleshooting

### 1. `ModuleNotFoundError: No module named 'src'`

**Solution:** Run from the project root, or add the project root to `PYTHONPATH`:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
# Windows: set PYTHONPATH=%PYTHONPATH%;%CD%
```

### 2. NLTK `LookupError` for `punkt` or `wordnet`

**Solution:** Download NLTK data manually:

```python
import nltk
nltk.download('punkt')
nltk.download('wordnet')
```

### 3. `FileNotFoundError: medical_dataset.csv not found`

**Solution:** Ensure the dataset is present at `data/raw/medical_dataset.csv`. If you cloned from a repository that uses Git LFS for large files, run:

```bash
git lfs pull
```

### 4. MySQL connection errors (`Can't connect to MySQL server`)

**Solution:**
- Verify MySQL is running: `sudo service mysql status` (Linux) or check Services (Windows).
- Verify credentials in `.env` match the MySQL user you created.
- Test manually: `mysql -u sma_user -p -h localhost smart_medical_db`

### 5. `ValueError: could not broadcast input array` during model training

**Solution:** Ensure the dataset was preprocessed successfully and `data/processed/` contains valid files. Re-run the preprocessing step if needed.

### 6. Port 5000 already in use

**Solution:** Change the port in `src/api/app.py` or run:

```bash
python -m src.api.app  # edit app.run(port=5001) in app.py if needed
```

Or use an environment variable:

```bash
export FLASK_RUN_PORT=5001
flask --app src.api.app run
```

### 7. CORS errors from frontend

**Solution:** Ensure `flask-cors` is installed and `CORS(app)` is present in `src/api/app.py`. The API already includes this, so verify the frontend URL is allowed if you customized CORS settings.

---

## Environment Variables

Create a `.env` file in the project root for local development. **Do not commit this file to version control.**

```bash
# .env — Smart Medical Assistant

# Flask
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_RUN_PORT=5000

# MySQL (optional)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=smart_medical_db
DB_USER=sma_user
DB_PASSWORD=YourSecurePassword123!

# Paths
MODEL_DIR=./models
DATA_DIR=./data/raw

# Frontend
REACT_APP_API_URL=http://localhost:5000
```

### Loading `.env` in Python

If you want the application to automatically load `.env`, install `python-dotenv`:

```bash
pip install python-dotenv
```

And add to `src/api/app.py` (already done if using modern Flask patterns):

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Activate venv (Linux/Mac) | `source venv/bin/activate` |
| Activate venv (Windows) | `venv\Scripts\activate` |
| Install deps | `pip install -r requirements.txt` |
| Preprocess data | `python -c "from src.utils.preprocessing import main; main({'runDir': os.getcwd()})"` |
| Train models | `python -c "from src.ml.train_models import main; main({'runDir': os.getcwd()})"` |
| Start API | `python -m src.api.app` |
| Run tests | `python -m pytest tests/ -v` |
| Run tests with coverage | `python -m pytest tests/ -v --cov=src` |

---

If you encounter any issues not covered above, please open an issue in the project repository or contact the maintainers.
