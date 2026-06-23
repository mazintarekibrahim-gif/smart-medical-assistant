SMART MEDICAL ASSISTANT - VS Code Setup Guide
=============================================

## Prerequisites
- Python 3.8+ installed on your computer
- VS Code installed
- Git installed (optional, for cloning)

## Step 1: Clone the Repository (or download ZIP)

```bash
git clone https://github.com/mazintarekibrahim-gif/smart-medical-assistant.git
cd smart-medical-assistant
```

Or download ZIP from GitHub and extract it.

## Step 2: Open in VS Code

```bash
code .
```

Or open VS Code → File → Open Folder → Select smart-medical-assistant

## Step 3: Create Virtual Environment

In VS Code Terminal (Ctrl+`):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install: Flask, scikit-learn, xgboost, nltk, pandas, numpy, matplotlib, seaborn, pytest, gunicorn

## Step 5: Download NLTK Data (One-time)

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
```

## Step 6: Run Preprocessing Pipeline

```bash
python -m src.utils.preprocessing
```

This will:
- Clean and tokenize the dataset
- Create TF-IDF features
- Save processed data to data/processed/
- Save preprocessor.pkl to models/

## Step 7: Train ML Models

```bash
python -m src.ml.train_models
```

This will:
- Train 6 ML models (Logistic Regression, Random Forest, Decision Tree, SVM, Naive Bayes, XGBoost)
- Generate comparison report
- Save best_model.pkl to models/
- Save comparison charts to reports/

## Step 8: Start Flask API (Backend)

```bash
python src/api/app.py
```

Or for the demo version (no sklearn required):
```bash
python src/api/demo_app.py
```

The API will be available at: http://localhost:5000

Check health: http://localhost:5000/api/health

## Step 9: Open Frontend

Option A: Open directly in browser
```bash
# Windows
start frontend/index.html

# Linux
xdg-open frontend/index.html

# Mac
open frontend/index.html
```

Option B: Use VS Code Live Server extension
- Install "Live Server" extension in VS Code
- Right-click on frontend/index.html → "Open with Live Server"

The frontend will open at: http://127.0.0.1:5500/frontend/index.html

## Step 10: Test the API

Using curl in terminal:
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I have fever, headache, and sore throat"}'
```

Or using the web interface directly.

## Step 11: Run Tests

```bash
python -m pytest tests/ -v
```

## Step 12: Stop the Server

Press Ctrl+C in the terminal running the API.

## Troubleshooting

### Issue: "No module named 'sklearn'"
**Solution:** Make sure virtual environment is activated:
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Issue: "Port 5000 already in use"
**Solution:** Change port in app.py or kill existing process:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### Issue: "CORS error in browser"
**Solution:** Make sure flask-cors is installed:
```bash
pip install flask-cors
```

### Issue: "NLTK data not found"
**Solution:** Download NLTK data:
```bash
python -c "import nltk; nltk.download('all')"
```

## Quick Reference Commands

```bash
# Setup (run once)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
python -m src.utils.preprocessing
python -m src.ml.train_models

# Daily usage
venv\Scripts\activate
python src/api/app.py
# Open frontend/index.html in browser
```

## VS Code Extensions Recommended
- Python (Microsoft)
- Python Docstring Generator
- Live Server
- Prettier
- Markdown All in One

## Project URLs When Running
- API Home: http://localhost:5000/
- API Health: http://localhost:5000/api/health
- API Predict: http://localhost:5000/api/predict (POST)
- API Analyze: http://localhost:5000/api/analyze (POST)
- API Diseases: http://localhost:5000/api/diseases
- API Symptoms: http://localhost:5000/api/symptoms
- Frontend: file://.../frontend/index.html or http://127.0.0.1:5500/frontend/

## Note for Graduation Project Defense
The project is ready to demonstrate with:
1. Dataset: 1,357 records, 30 diseases
2. EDA: 6 charts in reports/figures/
3. ML Models: 6 algorithms compared
4. NLP: 60+ symptom categories
5. API: 6 REST endpoints
6. Frontend: Professional responsive UI
7. Tests: 23 test cases
8. Documentation: 10 docs files + graduation book

---
Good luck with your graduation project! 🎓
