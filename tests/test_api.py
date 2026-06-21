"""
Integration tests for the Flask API backend.

Tests cover:
- Health endpoint availability
- Analyze endpoint with valid and missing text
- Predict endpoint (requires models or demo mode)
- Diseases endpoint
- Symptoms endpoint
- Error handling (missing fields, 404, 500)

Run with: python -m pytest tests/test_api.py -v
"""

import pytest
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api.app import app


@pytest.fixture
def client():
    """Provide a Flask test client configured for testing."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Tests for the /api/health endpoint."""

    def test_health_status_code(self, client):
        response = client.get('/api/health')
        assert response.status_code == 200

    def test_health_json_response(self, client):
        response = client.get('/api/health')
        data = response.get_json()
        assert data is not None
        assert data['status'] == 'healthy'

    def test_health_has_timestamp(self, client):
        response = client.get('/api/health')
        data = response.get_json()
        assert 'timestamp' in data
        assert isinstance(data['timestamp'], str)

    def test_health_models_loaded_key(self, client):
        response = client.get('/api/health')
        data = response.get_json()
        assert 'models_loaded' in data
        assert isinstance(data['models_loaded'], bool)


class TestAnalyzeEndpoint:
    """Tests for the /api/analyze endpoint."""

    def test_analyze_valid_text(self, client):
        payload = {'text': 'I have a fever and headache'}
        response = client.post('/api/analyze', json=payload)
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'fever' in data['extracted_symptoms'] or 'headache' in data['extracted_symptoms']

    def test_analyze_extracts_multiple_symptoms(self, client):
        payload = {'text': 'I have fever, headache, cough, and sore throat'}
        response = client.post('/api/analyze', json=payload)
        data = response.get_json()
        assert data['success'] is True
        assert len(data['extracted_symptoms']) >= 3

    def test_analyze_returns_confidence(self, client):
        payload = {'text': 'severe chest pain and shortness of breath'}
        response = client.post('/api/analyze', json=payload)
        data = response.get_json()
        assert 'confidence' in data
        assert 0.0 <= data['confidence'] <= 1.0

    def test_analyze_returns_severity(self, client):
        payload = {'text': 'I have a severe headache'}
        response = client.post('/api/analyze', json=payload)
        data = response.get_json()
        assert 'severity_detected' in data
        assert data['severity_detected'] == 'severe'

    def test_analyze_returns_model_input(self, client):
        payload = {'text': 'mild fever and cough'}
        response = client.post('/api/analyze', json=payload)
        data = response.get_json()
        assert 'model_input' in data
        assert isinstance(data['model_input'], str)

    def test_analyze_returns_recommendation(self, client):
        payload = {'text': 'I have a fever'}
        response = client.post('/api/analyze', json=payload)
        data = response.get_json()
        assert 'recommendation' in data
        assert 'level' in data['recommendation']
        assert 'message' in data['recommendation']
        assert 'action' in data['recommendation']

    def test_analyze_missing_text_field(self, client):
        payload = {'description': 'I have a fever'}
        response = client.post('/api/analyze', json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'text' in data['error'].lower()

    def test_analyze_empty_json(self, client):
        response = client.post('/api/analyze', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_analyze_no_json(self, client):
        response = client.post('/api/analyze')
        assert response.status_code == 400


class TestPredictEndpoint:
    """Tests for the /api/predict endpoint."""

    def test_predict_valid_text(self, client):
        payload = {'text': 'I have fever, headache, and body aches'}
        response = client.post('/api/predict', json=payload)
        data = response.get_json()
        # If models are loaded, expect 200; if not, expect 503
        assert response.status_code in [200, 503]
        if response.status_code == 200:
            assert data['success'] is True
            assert 'predictions' in data
            assert len(data['predictions']) > 0

    def test_predict_no_symptoms(self, client):
        payload = {'text': 'I am feeling happy today'}
        response = client.post('/api/predict', json=payload)
        data = response.get_json()
        if response.status_code == 200:
            assert data['success'] is True
            assert 'message' in data
            assert 'No symptoms were recognized' in data['message']

    def test_predict_missing_text_field(self, client):
        payload = {'include_details': True}
        response = client.post('/api/predict', json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_predict_structure_when_models_loaded(self, client):
        payload = {'text': 'severe chest pain and shortness of breath'}
        response = client.post('/api/predict', json=payload)
        if response.status_code == 200:
            data = response.get_json()
            assert 'extracted_symptoms' in data
            assert 'predictions' in data
            assert 'top_prediction' in data
            assert 'urgency_level' in data
            assert 'action_message' in data
            assert 'disclaimer' in data
            assert 'timestamp' in data

    def test_predict_top_prediction_has_disease(self, client):
        payload = {'text': 'I have fever and headache'}
        response = client.post('/api/predict', json=payload)
        if response.status_code == 200:
            data = response.get_json()
            top = data['top_prediction']
            assert 'disease' in top
            assert 'confidence' in top
            assert isinstance(top['confidence'], (int, float))

    def test_predict_include_details(self, client):
        payload = {'text': 'fever and cough', 'include_details': True}
        response = client.post('/api/predict', json=payload)
        if response.status_code == 200:
            data = response.get_json()
            preds = data['predictions']
            if len(preds) > 0:
                assert 'treatment' in preds[0]
                assert 'precautions' in preds[0]
                assert 'description' in preds[0]

    def test_predict_urgency_severe(self, client):
        payload = {'text': 'severe chest pain and shortness of breath'}
        response = client.post('/api/predict', json=payload)
        if response.status_code == 200:
            data = response.get_json()
            assert data['urgency_level'] in ['urgent', 'warning', 'caution']

    def test_predict_disclaimer_present(self, client):
        payload = {'text': 'headache'}
        response = client.post('/api/predict', json=payload)
        if response.status_code == 200:
            data = response.get_json()
            assert 'disclaimer' in data
            assert 'NOT a medical diagnosis' in data['disclaimer']


class TestDiseasesEndpoint:
    """Tests for the /api/diseases endpoint."""

    def test_diseases_status_code(self, client):
        response = client.get('/api/diseases')
        assert response.status_code in [200, 503]

    def test_diseases_returns_list(self, client):
        response = client.get('/api/diseases')
        if response.status_code == 200:
            data = response.get_json()
            assert data['success'] is True
            assert isinstance(data['diseases'], list)
            assert len(data['diseases']) > 0

    def test_diseases_has_count(self, client):
        response = client.get('/api/diseases')
        if response.status_code == 200:
            data = response.get_json()
            assert 'count' in data
            assert isinstance(data['count'], int)


class TestSymptomsEndpoint:
    """Tests for the /api/symptoms endpoint."""

    def test_symptoms_status_code(self, client):
        response = client.get('/api/symptoms')
        assert response.status_code == 200

    def test_symptoms_returns_list(self, client):
        response = client.get('/api/symptoms')
        data = response.get_json()
        assert data['success'] is True
        assert isinstance(data['symptoms'], list)
        assert len(data['symptoms']) > 0

    def test_symptoms_has_count(self, client):
        response = client.get('/api/symptoms')
        data = response.get_json()
        assert 'count' in data
        assert isinstance(data['count'], int)
        assert data['count'] == len(data['symptoms'])

    def test_symptoms_contains_known_symptoms(self, client):
        response = client.get('/api/symptoms')
        data = response.get_json()
        symptoms = data['symptoms']
        assert 'fever' in symptoms
        assert 'headache' in symptoms
        assert 'cough' in symptoms


class TestDiseaseDetailsEndpoint:
    """Tests for the /api/disease/<name> endpoint."""

    def test_disease_details_valid(self, client):
        response = client.get('/api/disease/Flu')
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.get_json()
            assert data['success'] is True
            assert 'disease' in data

    def test_disease_details_not_found(self, client):
        response = client.get('/api/disease/UnknownDiseaseXYZ')
        assert response.status_code == 404

    def test_disease_details_structure(self, client):
        response = client.get('/api/disease/Flu')
        if response.status_code == 200:
            data = response.get_json()
            assert 'treatment' in data
            assert 'precautions' in data
            assert 'description' in data
            assert 'severity' in data


class TestHomeEndpoint:
    """Tests for the root / endpoint."""

    def test_home_status_code(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_home_returns_api_info(self, client):
        response = client.get('/')
        data = response.get_json()
        assert data['status'] == 'online'
        assert 'Smart Medical Assistant' in data['service']
        assert 'endpoints' in data


class TestErrorHandlers:
    """Tests for API error handlers."""

    def test_404_handler(self, client):
        response = client.get('/api/nonexistent')
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'not found' in data['error'].lower()

    def test_405_method_not_allowed(self, client):
        response = client.get('/api/analyze')
        assert response.status_code == 405
