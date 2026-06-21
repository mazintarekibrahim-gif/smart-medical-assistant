"""
Flask API Backend for Smart Medical Assistant
Provides RESTful endpoints for symptom analysis and disease prediction
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import pickle
import numpy as np
import pandas as pd
from datetime import datetime

# Add project paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'nlp'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ml'))

from preprocessing import MedicalDataPreprocessor
from symptom_extractor import SymptomExtractor

app = Flask(__name__)
CORS(app)

# Load models and preprocessors
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw')

try:
    # Load preprocessor
    preprocessor = MedicalDataPreprocessor()
    preprocessor.load_preprocessor(os.path.join(MODEL_DIR, 'preprocessor.pkl'))
    
    # Load scaler
    with open(os.path.join(MODEL_DIR, 'scaler.pkl'), 'rb') as f:
        scaler = pickle.load(f)
    
    # Load best model
    with open(os.path.join(MODEL_DIR, 'best_model.pkl'), 'rb') as f:
        model = pickle.load(f)
    
    # Load dataset for treatment lookups
    df = pd.read_csv(os.path.join(DATA_DIR, 'medical_dataset.csv'))
    
    # Load feature names
    with open(os.path.join(MODEL_DIR, '..', 'data', 'processed', 'feature_names.txt'), 'r') as f:
        feature_names = [line.strip() for line in f.readlines()]
    
    MODELS_LOADED = True
    print("✓ All models loaded successfully")
    
except Exception as e:
    MODELS_LOADED = False
    print(f"⚠ Warning: Could not load models: {e}")
    print("API will run in demo mode")

# Initialize NLP extractor
extractor = SymptomExtractor()


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


@app.route('/')
def home():
    """API home endpoint."""
    return jsonify({
        'status': 'online',
        'service': 'Smart Medical Assistant API',
        'version': '1.0.0',
        'models_loaded': MODELS_LOADED,
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
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': MODELS_LOADED
    })


@app.route('/api/analyze', methods=['POST'])
def analyze_symptoms():
    """
    Analyze symptoms from natural language text.
    
    Request: {"text": "I have fever and headache"}
    Response: {"symptoms": [...], "confidence": 0.85, ...}
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing "text" field in request'}), 400
        
        text = data['text']
        
        # Run NLP extraction
        analysis = extractor.analyze(text)
        
        return jsonify({
            'success': True,
            'input': text,
            'extracted_symptoms': analysis['extraction']['extracted_symptoms'],
            'symptom_count': analysis['extraction']['symptom_count'],
            'confidence': analysis['extraction']['confidence'],
            'severity_detected': analysis['extraction']['severity'],
            'duration_detected': analysis['extraction']['duration'],
            'model_input': analysis['model_input'],
            'recommendation': analysis['recommendation']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict', methods=['POST'])
def predict_disease():
    """
    Predict disease from symptoms.
    
    Request: {"text": "I have fever and headache", "include_details": true}
    Response: {"disease": "Flu", "confidence": 0.92, ...}
    """
    if not MODELS_LOADED:
        return jsonify({'error': 'Models not loaded. API is in demo mode.'}), 503
    
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing "text" field in request'}), 400
        
        text = data['text']
        include_details = data.get('include_details', True)
        
        # Step 1: Extract symptoms using NLP
        analysis = extractor.analyze(text)
        extracted_symptoms = analysis['extraction']['extracted_symptoms']
        
        if not extracted_symptoms:
            return jsonify({
                'success': True,
                'predictions': [],
                'message': 'No symptoms were recognized. Please provide more details.',
                'recommendation': analysis['recommendation']
            })
        
        # Step 2: Format for ML model
        model_input_text = analysis['model_input']
        
        # Step 3: Preprocess for ML model
        processed_text = preprocessor.preprocess_text(model_input_text)
        
        # Get TF-IDF features
        tfidf_features = preprocessor.tfidf_vectorizer.transform([processed_text])
        
        # Add extra features
        symptom_count = len(extracted_symptoms)
        severity = analysis['extraction']['severity']
        severity_encoded = 0 if severity == 'mild' else (1 if severity == 'moderate' else 2) if severity else 1
        
        extra_features = np.array([[symptom_count, severity_encoded]])
        X_input = np.hstack([tfidf_features.toarray(), extra_features])
        X_input_scaled = scaler.transform(X_input)
        
        # Step 4: Get predictions
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(X_input_scaled)[0]
            top_indices = np.argsort(probabilities)[::-1][:5]
            
            predictions = []
            for idx in top_indices:
                disease_name = preprocessor.label_encoder.inverse_transform([idx])[0]
                confidence = float(probabilities[idx])
                
                pred = {
                    'disease': disease_name,
                    'confidence': round(confidence * 100, 2),
                    'severity': get_disease_info(disease_name)['severity']
                }
                
                if include_details:
                    info = get_disease_info(disease_name)
                    pred['treatment'] = info['treatment']
                    pred['precautions'] = info['precautions']
                    pred['description'] = info['description']
                
                predictions.append(pred)
            
            # Determine if urgent medical attention is needed
            top_confidence = predictions[0]['confidence']
            top_severity = predictions[0]['severity']
            
            if top_severity == 'Severe' and top_confidence > 80:
                urgency_level = 'urgent'
                action_message = '⚠️ This condition may require immediate medical attention. Please consult a doctor as soon as possible.'
            elif top_severity == 'Moderate' and top_confidence > 70:
                urgency_level = 'warning'
                action_message = 'Consider consulting a healthcare provider, especially if symptoms persist or worsen.'
            else:
                urgency_level = 'caution'
                action_message = 'Monitor your symptoms. If they worsen or new symptoms appear, consult a healthcare provider.'
            
            return jsonify({
                'success': True,
                'input': text,
                'extracted_symptoms': extracted_symptoms,
                'predictions': predictions,
                'top_prediction': predictions[0],
                'urgency_level': urgency_level,
                'action_message': action_message,
                'disclaimer': 'This is an AI-powered preliminary assessment and NOT a medical diagnosis. Always consult a qualified healthcare professional.',
                'timestamp': datetime.now().isoformat()
            })
        else:
            # Fallback for models without probability
            prediction = model.predict(X_input_scaled)[0]
            disease_name = preprocessor.label_encoder.inverse_transform([prediction])[0]
            
            return jsonify({
                'success': True,
                'input': text,
                'extracted_symptoms': extracted_symptoms,
                'predictions': [{'disease': disease_name, 'confidence': 85.0}],
                'top_prediction': {'disease': disease_name, 'confidence': 85.0},
                'urgency_level': 'caution',
                'action_message': 'Monitor your symptoms and consult a healthcare provider if needed.',
                'disclaimer': 'This is an AI-powered preliminary assessment and NOT a medical diagnosis. Always consult a qualified healthcare professional.',
                'timestamp': datetime.now().isoformat()
            })
        
    except Exception as e:
        import traceback
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    """Get list of all supported diseases."""
    if not MODELS_LOADED:
        return jsonify({'error': 'Models not loaded'}), 503
    
    diseases = list(preprocessor.label_encoder.classes_)
    return jsonify({
        'success': True,
        'count': len(diseases),
        'diseases': diseases
    })


@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    """Get list of all known symptoms."""
    symptoms = list(extractor.MEDICAL_SYMPTOMS.keys())
    return jsonify({
        'success': True,
        'count': len(symptoms),
        'symptoms': symptoms
    })


@app.route('/api/disease/<disease_name>', methods=['GET'])
def get_disease_details(disease_name):
    """Get detailed information about a specific disease."""
    info = get_disease_info(disease_name)
    if info['description'] == 'Information not available.':
        return jsonify({'error': 'Disease not found'}), 404
    
    return jsonify({
        'success': True,
        'disease': disease_name,
        **info
    })


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found', 'status': 404}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'status': 500}), 500


if __name__ == '__main__':
    print("Starting Smart Medical Assistant API...")
    print(f"Model directory: {MODEL_DIR}")
    print(f"Data directory: {DATA_DIR}")
    print(f"Models loaded: {MODELS_LOADED}")
    app.run(host='0.0.0.0', port=5000, debug=True)
