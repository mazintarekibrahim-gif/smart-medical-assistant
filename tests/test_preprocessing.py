"""
Unit tests for the MedicalDataPreprocessor module.

Tests cover:
- Text cleaning (lowercasing, special char removal, whitespace normalization)
- Tokenization
- Stopword removal
- Lemmatization
- Dataset-level preprocessing
- TF-IDF feature extraction
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Ensure project root is on path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.preprocessing import MedicalDataPreprocessor


@pytest.fixture
def preprocessor():
    """Provide a fresh MedicalDataPreprocessor instance per test."""
    return MedicalDataPreprocessor()


@pytest.fixture
def sample_dataframe():
    """Provide a small mock DataFrame that mimics the real dataset schema."""
    return pd.DataFrame({
        'Disease': ['Flu', 'Migraine', 'Allergy'],
        'Symptoms': [
            'Fever, headache, body aches, fatigue',
            'Severe headache, sensitivity to light, nausea',
            'Runny nose, sneezing, congestion'
        ],
        'Severity': ['Severe', 'Moderate', 'Mild']
    })


class TestCleanText:
    """Tests for clean_text method."""

    def test_clean_text_lowercasing(self, preprocessor):
        text = 'FEVER Headache AND Body Aches'
        result = preprocessor.clean_text(text)
        assert result == 'fever headache and body aches'

    def test_clean_text_removes_special_characters(self, preprocessor):
        text = 'fever@headache#body!aches'
        result = preprocessor.clean_text(text)
        assert '@' not in result
        assert '#' not in result
        assert '!' not in result
        assert result == 'feverheadachebodyaches'

    def test_clean_text_removes_numbers(self, preprocessor):
        text = 'fever 101 headache 2 days'
        result = preprocessor.clean_text(text)
        assert '101' not in result
        assert '2' not in result
        assert result == 'fever  headache  days'

    def test_clean_text_normalizes_whitespace(self, preprocessor):
        text = 'fever    headache\tbody\naches'
        result = preprocessor.clean_text(text)
        assert '  ' not in result
        assert result == 'fever headache body aches'

    def test_clean_text_empty_string(self, preprocessor):
        assert preprocessor.clean_text('') == ''

    def test_clean_text_none_input(self, preprocessor):
        assert preprocessor.clean_text(None) == ''

    def test_clean_text_numeric_input(self, preprocessor):
        result = preprocessor.clean_text(12345)
        assert result == ''


class TestTokenizeText:
    """Tests for tokenize_text method."""

    def test_tokenize_simple_sentence(self, preprocessor):
        text = 'fever headache cough'
        tokens = preprocessor.tokenize_text(text)
        assert tokens == ['fever', 'headache', 'cough']

    def test_tokenize_empty_string(self, preprocessor):
        tokens = preprocessor.tokenize_text('')
        assert tokens == []

    def test_tokenize_preserves_medical_terms(self, preprocessor):
        text = 'shortness of breath chest pain'
        tokens = preprocessor.tokenize_text(text)
        assert 'shortness' in tokens
        assert 'of' in tokens
        assert 'breath' in tokens


class TestRemoveStopwords:
    """Tests for remove_stopwords method."""

    def test_remove_common_stopwords(self, preprocessor):
        tokens = ['the', 'fever', 'and', 'headache', 'is', 'severe']
        filtered = preprocessor.remove_stopwords(tokens)
        assert 'the' not in filtered
        assert 'and' not in filtered
        assert 'is' not in filtered
        assert 'fever' in filtered
        assert 'headache' in filtered
        assert 'severe' in filtered

    def test_remove_short_tokens(self, preprocessor):
        tokens = ['a', 'fever', 'x', 'headache']
        filtered = preprocessor.remove_stopwords(tokens)
        assert 'a' not in filtered
        assert 'x' not in filtered
        assert 'fever' in filtered

    def test_empty_list(self, preprocessor):
        assert preprocessor.remove_stopwords([]) == []

    def test_all_stopwords_removed(self, preprocessor):
        tokens = ['i', 'have', 'a', 'the', 'and', 'of', 'with']
        filtered = preprocessor.remove_stopwords(tokens)
        assert filtered == []


class TestLemmatizeTokens:
    """Tests for lemmatize_tokens method."""

    def test_lemmatize_plural_to_singular(self, preprocessor):
        tokens = ['fevers', 'headaches', 'coughs']
        lemmatized = preprocessor.lemmatize_tokens(tokens)
        assert 'fever' in lemmatized
        assert 'headache' in lemmatized
        assert 'cough' in lemmatized

    def test_lemmatize_verb_forms(self, preprocessor):
        tokens = ['running', 'feeling', 'coughing']
        lemmatized = preprocessor.lemmatize_tokens(tokens)
        assert 'running' == lemmatized[0]  # WordNetLemmatizer without POS defaults to noun
        assert 'feeling' in lemmatized

    def test_empty_list(self, preprocessor):
        assert preprocessor.lemmatize_tokens([]) == []

    def test_lemmatize_preserves_base_words(self, preprocessor):
        tokens = ['fever', 'pain', 'cough']
        lemmatized = preprocessor.lemmatize_tokens(tokens)
        assert lemmatized == tokens


class TestPreprocessDataset:
    """Tests for preprocess_dataset method."""

    def test_preprocess_dataset_creates_symptoms_clean(self, preprocessor, sample_dataframe):
        df_processed = preprocessor.preprocess_dataset(sample_dataframe)
        assert 'Symptoms_Clean' in df_processed.columns
        assert all(df_processed['Symptoms_Clean'].apply(lambda x: isinstance(x, str)))

    def test_preprocess_dataset_encodes_disease(self, preprocessor, sample_dataframe):
        df_processed = preprocessor.preprocess_dataset(sample_dataframe)
        assert 'Disease_Encoded' in df_processed.columns
        assert df_processed['Disease_Encoded'].dtype in [np.int64, np.int32, int]
        assert len(df_processed['Disease_Encoded'].unique()) == 3

    def test_preprocess_dataset_encodes_severity(self, preprocessor, sample_dataframe):
        df_processed = preprocessor.preprocess_dataset(sample_dataframe)
        assert 'Severity_Encoded' in df_processed.columns
        assert df_processed['Severity_Encoded'].iloc[0] == 2  # Severe
        assert df_processed['Severity_Encoded'].iloc[1] == 1  # Moderate
        assert df_processed['Severity_Encoded'].iloc[2] == 0  # Mild

    def test_preprocess_dataset_adds_symptom_count(self, preprocessor, sample_dataframe):
        df_processed = preprocessor.preprocess_dataset(sample_dataframe)
        assert 'Symptom_Count' in df_processed.columns
        # First row has 4 symptoms (comma-separated)
        assert df_processed['Symptom_Count'].iloc[0] == 4

    def test_preprocess_dataset_extracts_severity_keywords(self, preprocessor, sample_dataframe):
        df_processed = preprocessor.preprocess_dataset(sample_dataframe)
        assert 'Severity_Keywords' in df_processed.columns
        # Row 1 contains 'Severe' in the severity column, but the keyword extraction
        # looks at the Symptoms column. Row 1 has 'Severe headache' so high_severity
        assert 'high_severity' in df_processed['Severity_Keywords'].iloc[1]

    def test_preprocess_dataset_preserves_original_data(self, preprocessor, sample_dataframe):
        df_processed = preprocessor.preprocess_dataset(sample_dataframe)
        assert 'Disease' in df_processed.columns
        assert 'Symptoms' in df_processed.columns
        assert 'Severity' in df_processed.columns
        assert len(df_processed) == len(sample_dataframe)

    def test_preprocess_dataset_empty_dataframe(self, preprocessor):
        empty_df = pd.DataFrame(columns=['Disease', 'Symptoms', 'Severity'])
        df_processed = preprocessor.preprocess_dataset(empty_df)
        assert len(df_processed) == 0
        assert 'Symptoms_Clean' in df_processed.columns


class TestExtractFeatures:
    """Tests for extract_features method."""

    def test_extract_features_returns_tfidf_matrix(self, preprocessor, sample_dataframe):
        df_processed = preprocessor.preprocess_dataset(sample_dataframe)
        tfidf_matrix, tfidf_df, feature_names = preprocessor.extract_features(df_processed)
        assert tfidf_matrix is not None
        assert tfidf_matrix.shape[0] == len(sample_dataframe)
        assert tfidf_matrix.shape[1] > 0

    def test_extract_features_returns_dataframe(self, preprocessor, sample_dataframe):
        df_processed = preprocessor.preprocess_dataset(sample_dataframe)
        tfidf_matrix, tfidf_df, feature_names = preprocessor.extract_features(df_processed)
        assert isinstance(tfidf_df, pd.DataFrame)
        assert tfidf_df.shape[0] == len(sample_dataframe)
        assert tfidf_df.shape[1] == len(feature_names)

    def test_extract_features_column_prefix(self, preprocessor, sample_dataframe):
        df_processed = preprocessor.preprocess_dataset(sample_dataframe)
        tfidf_matrix, tfidf_df, feature_names = preprocessor.extract_features(df_processed)
        assert all(col.startswith('tfidf_') for col in tfidf_df.columns)

    def test_extract_features_max_features(self, preprocessor, sample_dataframe):
        df_processed = preprocessor.preprocess_dataset(sample_dataframe)
        tfidf_matrix, tfidf_df, feature_names = preprocessor.extract_features(df_processed, max_features=10)
        assert len(feature_names) <= 10

    def test_extract_features_vectorizer_is_trained(self, preprocessor, sample_dataframe):
        df_processed = preprocessor.preprocess_dataset(sample_dataframe)
        preprocessor.extract_features(df_processed)
        assert preprocessor.tfidf_vectorizer is not None

    def test_preprocess_text_full_pipeline(self, preprocessor):
        raw = 'The patient has a FEVER and severe HEADACHE!!!'
        result = preprocessor.preprocess_text(raw)
        assert 'fever' in result
        assert 'headache' in result
        assert '!!!' not in result
        assert 'The' not in result
        assert 'patient' not in result  # It's a stopword in the extended list
        assert 'has' not in result
        assert 'and' not in result
        assert 'severe' in result
