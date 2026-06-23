"""
Simple Flask API for Smart Medical Assistant (Demo Mode - No sklearn required)
This version runs without ML dependencies, using keyword matching from the dataset.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load dataset directly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'medical_dataset.csv')

# Load data
try:
    df = pd.read_csv(DATA_PATH)
    print(f"✓ Loaded dataset: {len(df)} records, {df['Disease'].nunique()} diseases")
    DATA_LOADED = True
except Exception as e:
    print(f"⚠ Could not load dataset: {e}")
    DATA_LOADED = False

# Simple symptom mapping (60+ symptoms)
SYMPTOM_MAP = {
    'fever': ['fever', 'high temperature', 'temperature'],
    'headache': ['headache', 'head pain', 'migraine', 'head ache'],
    'cough': ['cough', 'coughing', 'dry cough', 'wet cough'],
    'sore throat': ['sore throat', 'throat pain', 'painful throat', 'scratchy throat'],
    'runny nose': ['runny nose', 'runny nostrils', 'nasal discharge', 'dripping nose'],
    'sneezing': ['sneezing', 'sneezes'],
    'congestion': ['congestion', 'stuffy nose', 'nasal congestion', 'blocked nose'],
    'body aches': ['body aches', 'body pain', 'muscle pain', 'muscle aches', 'myalgia', 'sore muscles'],
    'fatigue': ['fatigue', 'tired', 'exhaustion', 'lethargy', 'no energy', 'tiredness', 'weakness'],
    'chills': ['chills', 'shivering', 'shaking', 'rigors'],
    'nausea': ['nausea', 'nauseated', 'feeling sick', 'queasy', 'upset stomach'],
    'vomiting': ['vomiting', 'throwing up', 'puking', 'emesis', 'retching'],
    'diarrhea': ['diarrhea', 'loose stools', 'watery stools', 'frequent stools'],
    'constipation': ['constipation', 'hard stools', 'difficulty passing stool'],
    'chest pain': ['chest pain', 'chest tightness', 'pressure in chest', 'chest discomfort'],
    'shortness of breath': ['shortness of breath', 'breathing difficulty', 'difficulty breathing', 'dyspnea', 'cannot breathe', 'trouble breathing', 'breathlessness'],
    'dizziness': ['dizziness', 'lightheaded', 'vertigo', 'spinning', 'unsteady', 'feeling faint'],
    'loss of taste': ['loss of taste', 'no taste', 'tasteless', 'cannot taste'],
    'loss of smell': ['loss of smell', 'no smell', 'anosmia', 'cannot smell'],
    'abdominal pain': ['abdominal pain', 'stomach pain', 'belly pain', 'tummy ache', 'stomach ache', 'abdominal cramps', 'stomach cramps'],
    'jaundice': ['jaundice', 'yellow skin', 'yellow eyes', 'yellowing'],
    'joint pain': ['joint pain', 'arthralgia', 'aching joints', 'painful joints', 'joint swelling', 'swollen joints', 'stiff joints'],
    'swelling': ['swelling', 'edema', 'puffy', 'bloating', 'swollen', 'water retention'],
    'weight loss': ['weight loss', 'losing weight', 'unexplained weight loss', 'rapid weight loss'],
    'weight gain': ['weight gain', 'gaining weight', 'unexplained weight gain'],
    'thirst': ['thirst', 'excessive thirst', 'very thirsty', 'polydipsia', 'always thirsty'],
    'frequent urination': ['frequent urination', 'urinating often', 'polyuria', 'peeing a lot'],
    'burning urination': ['burning urination', 'painful urination', 'dysuria', 'burning when peeing'],
    'blood in urine': ['blood in urine', 'hematuria', 'bloody urine', 'red urine', 'pink urine'],
    'blurred vision': ['blurred vision', 'blurry vision', 'vision problems', 'double vision', 'seeing blurry', 'visual disturbance'],
    'numbness': ['numbness', 'tingling', 'pins and needles', 'paresthesia', 'loss of sensation', 'numb'],
    'confusion': ['confusion', 'disoriented', 'mental fog', 'memory problems', 'confused', 'delirium', 'altered mental state'],
    'depression': ['depression', 'sadness', 'hopelessness', 'low mood', 'feeling down', 'persistent sadness', 'depressed mood'],
    'anxiety': ['anxiety', 'worry', 'nervousness', 'panic', 'fear', 'unease', 'apprehension', 'restlessness', 'anxious'],
    'insomnia': ['insomnia', 'cannot sleep', 'sleep problems', 'sleeplessness', 'difficulty sleeping', 'poor sleep', 'sleep disturbance'],
    'sweating': ['sweating', 'excessive sweating', 'night sweats', 'perspiration', 'hyperhidrosis', 'profuse sweating'],
    'appetite loss': ['appetite loss', 'loss of appetite', 'not hungry', 'anorexia', 'decreased appetite', 'no appetite'],
    'heart palpitations': ['heart palpitations', 'racing heart', 'irregular heartbeat', 'fluttering', 'heart pounding', 'tachycardia'],
    'back pain': ['back pain', 'lower back pain', 'upper back pain', 'spinal pain', 'lumbar pain', 'back ache'],
    'stiffness': ['stiffness', 'joint stiffness', 'morning stiffness', 'rigid', 'tight muscles', 'reduced mobility'],
    'wheezing': ['wheezing', 'wheezed', 'wheeze', 'noisy breathing', 'whistling sound'],
    'chest tightness': ['chest tightness', 'chest pressure', 'constricted chest', 'chest heaviness', 'tight chest'],
    'sensitivity to light': ['sensitivity to light', 'photophobia', 'light hurts', 'bright light sensitivity'],
    'sensitivity to sound': ['sensitivity to sound', 'phonophobia', 'noise sensitivity', 'sounds hurt'],
    'throbbing pain': ['throbbing pain', 'pulsating pain', 'throbbing headache', 'pounding pain'],
    'visual aura': ['visual aura', 'seeing spots', 'flashing lights', 'zigzag lines', 'blind spots', 'visual disturbances'],
    'nosebleeds': ['nosebleeds', 'nose bleeding', 'epistaxis', 'bloody nose'],
    'flushing': ['flushing', 'red face', 'facial redness', 'hot flashes', 'blushing', 'face feels hot'],
    'slow healing': ['slow healing', 'wounds not healing', 'poor wound healing', 'delayed healing'],
    'hair loss': ['hair loss', 'alopecia', 'thinning hair', 'losing hair', 'baldness', 'hair falling out'],
    'dry skin': ['dry skin', 'skin dryness', 'xerosis', 'flaky skin', 'rough skin'],
    'cold sensitivity': ['cold sensitivity', 'cold intolerance', 'always cold', 'feeling cold', 'cold hands', 'cold feet'],
    'heat sensitivity': ['heat sensitivity', 'heat intolerance', 'always hot', 'feeling hot', 'sweating in heat'],
    'tremor': ['tremor', 'shaking', 'trembling', 'shaky hands', 'involuntary shaking', 'quivering'],
    'bulging eyes': ['bulging eyes', 'proptosis', 'eye bulging', 'prominent eyes', 'eyes sticking out'],
    'difficulty concentrating': ['difficulty concentrating', 'cannot focus', 'brain fog', 'poor concentration', 'trouble focusing', 'attention problems'],
    'feelings of worthlessness': ['feelings of worthlessness', 'feeling worthless', 'self-loathing', 'guilt', 'inadequacy', 'self-criticism'],
    'thoughts of death': ['thoughts of death', 'suicidal thoughts', 'wanting to die', 'death ideation', 'suicidal ideation'],
    'panic attacks': ['panic attacks', 'panic', 'sudden fear', 'terror', 'overwhelming anxiety', 'panic episodes'],
    'irritability': ['irritability', 'easily annoyed', 'short temper', 'mood swings', 'agitation', 'frustration'],
    'muscle tension': ['muscle tension', 'tense muscles', 'muscle tightness', 'muscle knots', 'tight muscles'],
    'sleep disturbances': ['sleep disturbances', 'sleeping problems', 'restless sleep', 'waking up early', 'broken sleep']
}

def extract_symptoms(text):
    """Extract symptoms from text using simple keyword matching."""
    text_lower = text.lower()
    extracted = []
    matched_phrases = []
    
    for canonical, variations in SYMPTOM_MAP.items():
        for variant in variations:
            if variant in text_lower:
                if canonical not in extracted:
                    extracted.append(canonical)
                    matched_phrases.append(variant)
                break
    
    # Severity detection
    severity = None
    if any(w in text_lower for w in ['severe', 'extreme', 'intense', 'unbearable', 'terrible', 'awful', 'worst', 'agonizing', 'crippling', 'debilitating', 'incapacitating', 'worsening', 'persistent', 'constant']):
        severity = 'Severe'
    elif any(w in text_lower for w in ['moderate', 'fairly', 'quite', 'rather', 'uncomfortable', 'noticeable', 'significant']):
        severity = 'Moderate'
    elif any(w in text_lower for w in ['mild', 'slight', 'minor', 'a little', 'somewhat', 'tolerable', 'bearable', 'light', 'occasional']):
        severity = 'Mild'
    
    # Duration detection
    duration = None
    if any(w in text_lower for w in ['weeks', 'months', 'years', 'long time', 'chronic', 'ongoing', 'persistent', 'recurring', 'for years']):
        duration = 'Chronic'
    elif any(w in text_lower for w in ['few days', 'couple days', 'three days', 'four days', 'last week', 'about a week', 'started recently']):
        duration = 'Subacute'
    elif any(w in text_lower for w in ['sudden', 'abrupt', 'recent', 'today', 'just started', 'few hours', 'since yesterday', 'last night', 'this morning']):
        duration = 'Acute'
    
    # Confidence
    if len(extracted) >= 5:
        confidence = 0.95
    elif len(extracted) >= 3:
        confidence = 0.85
    elif len(extracted) >= 2:
        confidence = 0.70
    elif len(extracted) >= 1:
        confidence = 0.50
    else:
        confidence = 0.0
    
    if severity and len(extracted) > 0:
        confidence = min(0.99, confidence + 0.05)
    
    return {
        'extracted_symptoms': extracted,
        'matched_phrases': matched_phrases,
        'confidence': round(confidence, 2),
        'severity': severity,
        'duration': duration,
        'symptom_count': len(extracted)
    }

def get_disease_info(disease_name):
    """Get treatment and precaution information for a disease."""
    disease_data = df[df['Disease'] == disease_name]
    if len(disease_data) > 0:
        return {
            'treatment': disease_data.iloc[0]['Recommended_Treatment'],
            'precautions': disease_data.iloc[0]['Precautions'],
            'description': disease_data.iloc[0]['Description'],
            'severity': disease_data.iloc[0]['Severity']
        }
    return {
        'treatment': 'Consult a healthcare provider for appropriate treatment.',
        'precautions': 'Monitor symptoms and seek medical advice if condition worsens.',
        'description': 'Information not available.',
        'severity': 'Unknown'
    }

def predict_disease_from_symptoms(extracted_symptoms):
    """Predict disease by matching symptoms in dataset."""
    if not extracted_symptoms:
        return []
    
    # Score each disease by symptom overlap
    disease_scores = {}
    for disease in df['Disease'].unique():
        disease_records = df[df['Disease'] == disease]
        all_disease_symptoms = set()
        for symptoms_text in disease_records['Symptoms']:
            all_disease_symptoms.update(s.strip().lower() for s in str(symptoms_text).split(','))
        
        # Count matches
        matches = 0
        for user_symptom in extracted_symptoms:
            for disease_symptom in all_disease_symptoms:
                if user_symptom in disease_symptom or disease_symptom in user_symptom:
                    matches += 1
                    break
        
        # Normalize score
        disease_symptom_count = len(all_disease_symptoms)
        if disease_symptom_count > 0:
            score = matches / max(len(extracted_symptoms), disease_symptom_count)
        else:
            score = 0
        
        disease_scores[disease] = score
    
    # Sort by score, get top 5
    sorted_diseases = sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)
    top_5 = sorted_diseases[:5]
    
    predictions = []
    for disease, score in top_5:
        confidence = round(score * 100, 2)
        if confidence > 0:
            info = get_disease_info(disease)
            predictions.append({
                'disease': disease,
                'confidence': confidence,
                'severity': info['severity'],
                'treatment': info['treatment'],
                'precautions': info['precautions'],
                'description': info['description']
            })
    
    return predictions


@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'service': 'Smart Medical Assistant API (Demo Mode)',
        'version': '1.0.0',
        'data_loaded': DATA_LOADED,
        'endpoints': [
            '/api/health',
            '/api/analyze',
            '/api/predict',
            '/api/diseases',
            '/api/symptoms'
        ]
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'data_loaded': DATA_LOADED
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_symptoms():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing "text" field in request'}), 400
        
        text = data['text']
        extraction = extract_symptoms(text)
        
        # Generate recommendation
        if extraction['symptom_count'] == 0:
            recommendation = {
                'level': 'info',
                'message': 'No symptoms were recognized.',
                'action': 'Please describe symptoms like "fever", "headache", or "cough".'
            }
        elif extraction['severity'] == 'Severe':
            recommendation = {
                'level': 'urgent',
                'message': f'{extraction["symptom_count"]} symptoms with severe intensity.',
                'action': 'This may require immediate medical attention. Consult a doctor ASAP.'
            }
        elif extraction['symptom_count'] >= 5:
            recommendation = {
                'level': 'warning',
                'message': f'Multiple symptoms ({extraction["symptom_count"]}) detected.',
                'action': 'Consider consulting a healthcare provider if symptoms persist.'
            }
        else:
            recommendation = {
                'level': 'caution',
                'message': f'{extraction["symptom_count"]} symptom(s) detected.',
                'action': 'Monitor symptoms. Consult a provider if they worsen.'
            }
        
        return jsonify({
            'success': True,
            'input': text,
            'extracted_symptoms': extraction['extracted_symptoms'],
            'symptom_count': extraction['symptom_count'],
            'confidence': extraction['confidence'],
            'severity_detected': extraction['severity'],
            'duration_detected': extraction['duration'],
            'model_input': ', '.join(extraction['extracted_symptoms']),
            'recommendation': recommendation
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict_disease():
    if not DATA_LOADED:
        return jsonify({'error': 'Dataset not loaded. API is in demo mode.'}), 503
    
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing "text" field in request'}), 400
        
        text = data['text']
        include_details = data.get('include_details', True)
        
        # Extract symptoms
        extraction = extract_symptoms(text)
        extracted_symptoms = extraction['extracted_symptoms']
        
        if not extracted_symptoms:
            return jsonify({
                'success': True,
                'predictions': [],
                'message': 'No symptoms recognized. Please provide more details.',
                'recommendation': {
                    'level': 'info',
                    'action': 'Please describe specific symptoms like "fever", "headache", or "cough".'
                }
            })
        
        # Predict disease
        predictions = predict_disease_from_symptoms(extracted_symptoms)
        
        if not predictions:
            return jsonify({
                'success': True,
                'input': text,
                'extracted_symptoms': extracted_symptoms,
                'predictions': [],
                'message': 'Could not match symptoms to known diseases.',
                'recommendation': {
                    'level': 'warning',
                    'action': 'Please consult a healthcare provider for accurate diagnosis.'
                }
            })
        
        # Determine urgency
        top_prediction = predictions[0]
        top_severity = top_prediction['severity']
        top_confidence = top_prediction['confidence']
        
        if top_severity == 'Severe' and top_confidence > 70:
            urgency_level = 'urgent'
            action_message = '⚠️ This condition may require immediate medical attention. Please consult a doctor as soon as possible.'
        elif top_severity == 'Moderate' and top_confidence > 50:
            urgency_level = 'warning'
            action_message = 'Consider consulting a healthcare provider, especially if symptoms persist or worsen.'
        else:
            urgency_level = 'caution'
            action_message = 'Monitor your symptoms. If they worsen or new symptoms appear, consult a healthcare provider.'
        
        # Strip details if not requested
        if not include_details:
            for p in predictions:
                del p['treatment']
                del p['precautions']
                del p['description']
        
        return jsonify({
            'success': True,
            'input': text,
            'extracted_symptoms': extracted_symptoms,
            'predictions': predictions,
            'top_prediction': top_prediction,
            'urgency_level': urgency_level,
            'action_message': action_message,
            'disclaimer': 'This is an AI-powered preliminary assessment and NOT a medical diagnosis. Always consult a qualified healthcare professional.',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    if not DATA_LOADED:
        return jsonify({'error': 'Dataset not loaded'}), 503
    
    diseases = sorted(df['Disease'].unique().tolist())
    return jsonify({
        'success': True,
        'count': len(diseases),
        'diseases': diseases
    })

@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    symptoms = sorted(list(SYMPTOM_MAP.keys()))
    return jsonify({
        'success': True,
        'count': len(symptoms),
        'symptoms': symptoms
    })

@app.route('/api/disease/<disease_name>', methods=['GET'])
def get_disease_details(disease_name):
    if not DATA_LOADED:
        return jsonify({'error': 'Dataset not loaded'}), 503
    
    info = get_disease_info(disease_name)
    if info['description'] == 'Information not available.':
        return jsonify({'error': 'Disease not found'}), 404
    
    return jsonify({
        'success': True,
        'disease': disease_name,
        **info
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found', 'status': 404}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'status': 500}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("SMART MEDICAL ASSISTANT API (DEMO MODE)")
    print("=" * 60)
    print(f"Data loaded: {DATA_LOADED}")
    print(f"Dataset: {len(df) if DATA_LOADED else 0} records")
    print(f"Diseases: {df['Disease'].nunique() if DATA_LOADED else 0}")
    print(f"Symptoms: {len(SYMPTOM_MAP)}")
    print(f"API URL: http://localhost:5000")
    print(f"Health:  http://localhost:5000/api/health")
    print(f"Predict: http://localhost:5000/api/predict")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
