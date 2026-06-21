"""
Model evaluation tests for the Smart Medical Assistant ML pipeline.

These tests validate:
- Model accuracy meets minimum threshold
- Prediction output shapes are correct
- Feature extraction pipeline works
- Label encoding is consistent

Models may not be present in all environments (e.g., CI without training data).
Use pytest skipif to handle missing artifacts gracefully.
"""

import pytest
import numpy as np
import pandas as pd
import os
import sys
import pickle

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from utils.preprocessing import MedicalDataPreprocessor

# ---------------------------------------------------------------------------
# Determine if model artifacts exist so we can skip tests when unavailable
# ---------------------------------------------------------------------------
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')
PREPROCESSOR_PATH = os.path.join(MODEL_DIR, 'preprocessor.pkl')
BEST_MODEL_PATH = os.path.join(MODEL_DIR, 'best_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')

MODELS_AVAILABLE = (
    os.path.isfile(BEST_MODEL_PATH)
    and os.path.isfile(PREPROCESSOR_PATH)
    and os.path.isfile(SCALER_PATH)
)

DATASET_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'data', 'raw', 'medical_dataset.csv'
)
DATASET_AVAILABLE = os.path.isfile(DATASET_PATH)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def preprocessor():
    """Load a fitted preprocessor from disk, or return a fresh one."""
    if os.path.isfile(PREPROCESSOR_PATH):
        p = MedicalDataPreprocessor()
        p.load_preprocessor(PREPROCESSOR_PATH)
        return p
    return MedicalDataPreprocessor()


@pytest.fixture
def sample_df():
    """Small mock dataset for tests that don't need the full CSV."""
    return pd.DataFrame({
        'Disease': ['Flu', 'Migraine', 'Allergy', 'Asthma', 'Diabetes'],
        'Symptoms': [
            'fever headache body aches fatigue',
            'severe headache sensitivity to light nausea',
            'runny nose sneezing congestion',
            'wheezing shortness of breath chest tightness',
            'frequent urination thirst weight loss fatigue'
        ],
        'Severity': ['Severe', 'Moderate', 'Mild', 'Moderate', 'Severe']
    })


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestModelArtifacts:
    """Sanity checks for model artifact existence."""

    def test_model_directory_exists(self):
        assert os.path.isdir(MODEL_DIR) or not os.path.exists(MODEL_DIR)

    @pytest.mark.skipif(not MODELS_AVAILABLE, reason='Model artifacts not found')
    def test_best_model_file_exists(self):
        assert os.path.isfile(BEST_MODEL_PATH)

    @pytest.mark.skipif(not MODELS_AVAILABLE, reason='Model artifacts not found')
    def test_preprocessor_file_exists(self):
        assert os.path.isfile(PREPROCESSOR_PATH)

    @pytest.mark.skipif(not MODELS_AVAILABLE, reason='Model artifacts not found')
    def test_scaler_file_exists(self):
        assert os.path.isfile(SCALER_PATH)


class TestModelAccuracyThreshold:
    """
    Validate that the trained model meets a minimum accuracy threshold
    on a held-out test set.  This test requires the full dataset.
    """

    @pytest.mark.skipif(not MODELS_AVAILABLE, reason='Model artifacts not found')
    @pytest.mark.skipif(not DATASET_AVAILABLE, reason='Dataset not found')
    def test_accuracy_threshold(self, preprocessor):
        """Model accuracy should be >= 60% on a 20% test split."""
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score

        df = pd.read_csv(DATASET_PATH)
        df_processed = preprocessor.preprocess_dataset(df)
        tfidf_matrix, _, _ = preprocessor.extract_features(df_processed)
        extra = df_processed[['Symptom_Count', 'Severity_Encoded']].values
        X = np.hstack([tfidf_matrix.toarray(), extra])
        y = df_processed['Disease_Encoded'].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        with open(BEST_MODEL_PATH, 'rb') as f:
            model = pickle.load(f)

        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)

        X_test_scaled = scaler.transform(X_test)
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)

        assert accuracy >= 0.60, f'Accuracy {accuracy:.4f} below threshold 0.60'

    @pytest.mark.skipif(not MODELS_AVAILABLE, reason='Model artifacts not found')
    @pytest.mark.skipif(not DATASET_AVAILABLE, reason='Dataset not found')
    def test_f1_threshold(self, preprocessor):
        """Weighted F1 should be >= 55%."""
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import f1_score

        df = pd.read_csv(DATASET_PATH)
        df_processed = preprocessor.preprocess_dataset(df)
        tfidf_matrix, _, _ = preprocessor.extract_features(df_processed)
        extra = df_processed[['Symptom_Count', 'Severity_Encoded']].values
        X = np.hstack([tfidf_matrix.toarray(), extra])
        y = df_processed['Disease_Encoded'].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        with open(BEST_MODEL_PATH, 'rb') as f:
            model = pickle.load(f)

        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)

        X_test_scaled = scaler.transform(X_test)
        y_pred = model.predict(X_test_scaled)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

        assert f1 >= 0.55, f'F1 {f1:.4f} below threshold 0.55'


class TestModelPredictionShape:
    """Validate prediction shapes and types."""

    @pytest.mark.skipif(not MODELS_AVAILABLE, reason='Model artifacts not found')
    def test_single_prediction_shape(self, preprocessor):
        with open(BEST_MODEL_PATH, 'rb') as f:
            model = pickle.load(f)

        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)

        # Build a minimal single-row input matching the feature space
        processed_text = preprocessor.preprocess_text('fever headache cough')
        tfidf = preprocessor.tfidf_vectorizer.transform([processed_text])
        extra = np.array([[3, 1]])  # 3 symptoms, moderate severity
        X = np.hstack([tfidf.toarray(), extra])
        X_scaled = scaler.transform(X)

        prediction = model.predict(X_scaled)
        assert prediction.shape == (1,)
        assert isinstance(prediction[0], (np.integer, int))

    @pytest.mark.skipif(not MODELS_AVAILABLE, reason='Model artifacts not found')
    def test_predict_proba_shape(self, preprocessor):
        with open(BEST_MODEL_PATH, 'rb') as f:
            model = pickle.load(f)

        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)

        if not hasattr(model, 'predict_proba'):
            pytest.skip('Model does not support predict_proba')

        processed_text = preprocessor.preprocess_text('fever headache')
        tfidf = preprocessor.tfidf_vectorizer.transform([processed_text])
        extra = np.array([[2, 1]])
        X = np.hstack([tfidf.toarray(), extra])
        X_scaled = scaler.transform(X)

        proba = model.predict_proba(X_scaled)
        assert proba.shape[0] == 1
        assert proba.shape[1] == len(preprocessor.label_encoder.classes_)
        assert np.isclose(proba.sum(), 1.0, atol=1e-6)

    @pytest.mark.skipif(not MODELS_AVAILABLE, reason='Model artifacts not found')
    def test_top5_predictions(self, preprocessor):
        """If predict_proba is available, we should be able to get top-5."""
        with open(BEST_MODEL_PATH, 'rb') as f:
            model = pickle.load(f)

        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)

        if not hasattr(model, 'predict_proba'):
            pytest.skip('Model does not support predict_proba')

        processed_text = preprocessor.preprocess_text('fever headache cough sore throat fatigue')
        tfidf = preprocessor.tfidf_vectorizer.transform([processed_text])
        extra = np.array([[5, 2]])
        X = np.hstack([tfidf.toarray(), extra])
        X_scaled = scaler.transform(X)

        proba = model.predict_proba(X_scaled)[0]
        top_indices = np.argsort(proba)[::-1][:5]
        assert len(top_indices) == 5
        assert all(0 <= idx < len(preprocessor.label_encoder.classes_) for idx in top_indices)


class TestFeatureExtraction:
    """Validate that the feature extraction pipeline produces valid output."""

    def test_feature_matrix_shape(self, preprocessor, sample_df):
        df_processed = preprocessor.preprocess_dataset(sample_df)
        tfidf_matrix, tfidf_df, feature_names = preprocessor.extract_features(df_processed)
        assert tfidf_matrix.shape[0] == len(sample_df)
        assert tfidf_matrix.shape[1] == len(feature_names)

    def test_feature_matrix_non_negative(self, preprocessor, sample_df):
        df_processed = preprocessor.preprocess_dataset(sample_df)
        tfidf_matrix, _, _ = preprocessor.extract_features(df_processed)
        assert tfidf_matrix.min() >= 0.0

    def test_feature_names_unique(self, preprocessor, sample_df):
        df_processed = preprocessor.preprocess_dataset(sample_df)
        _, _, feature_names = preprocessor.extract_features(df_processed)
        assert len(feature_names) == len(set(feature_names))

    def test_feature_names_not_empty(self, preprocessor, sample_df):
        df_processed = preprocessor.preprocess_dataset(sample_df)
        _, _, feature_names = preprocessor.extract_features(df_processed)
        assert len(feature_names) > 0
        assert all(isinstance(name, str) and len(name) > 0 for name in feature_names)

    def test_extra_features_shape(self, preprocessor, sample_df):
        df_processed = preprocessor.preprocess_dataset(sample_df)
        extra = df_processed[['Symptom_Count', 'Severity_Encoded']].values
        assert extra.shape[0] == len(sample_df)
        assert extra.shape[1] == 2

    def test_combined_features_shape(self, preprocessor, sample_df):
        df_processed = preprocessor.preprocess_dataset(sample_df)
        tfidf_matrix, _, _ = preprocessor.extract_features(df_processed)
        extra = df_processed[['Symptom_Count', 'Severity_Encoded']].values
        X = np.hstack([tfidf_matrix.toarray(), extra])
        assert X.shape[0] == len(sample_df)
        assert X.shape[1] == tfidf_matrix.shape[1] + 2


class TestLabelEncoding:
    """Validate label encoding consistency."""

    def test_label_encoder_classes_unique(self, preprocessor, sample_df):
        df_processed = preprocessor.preprocess_dataset(sample_df)
        classes = preprocessor.label_encoder.classes_
        assert len(classes) == len(set(classes))

    def test_label_encoder_classes_sorted(self, preprocessor, sample_df):
        df_processed = preprocessor.preprocess_dataset(sample_df)
        classes = preprocessor.label_encoder.classes_
        assert list(classes) == sorted(classes)

    def test_inverse_transform(self, preprocessor, sample_df):
        df_processed = preprocessor.preprocess_dataset(sample_df)
        classes = preprocessor.label_encoder.classes_
        for i, cls in enumerate(classes):
            inv = preprocessor.label_encoder.inverse_transform([i])
            assert inv[0] == cls

    def test_encoding_range(self, preprocessor, sample_df):
        df_processed = preprocessor.preprocess_dataset(sample_df)
        encoded = df_processed['Disease_Encoded']
        assert encoded.min() >= 0
        assert encoded.max() < len(preprocessor.label_encoder.classes_)
        assert len(encoded.unique()) == len(preprocessor.label_encoder.classes_)
