"""
Data Preprocessing Pipeline for Smart Medical Assistant
"""

import pandas as pd
import numpy as np
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

class MedicalDataPreprocessor:
    """
    Comprehensive preprocessing pipeline for medical text data.
    """
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        # Add medical-specific stopwords
        self.stop_words.update(['i', 'have', 'had', 'been', 'feel', 'feeling', 'a', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'from', 'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just', 'should', 'now'])
        
        self.label_encoder = LabelEncoder()
        self.tfidf_vectorizer = None
        
    def clean_text(self, text):
        """
        Clean and normalize raw text.
        
        Steps:
        1. Lowercase
        2. Remove special characters and numbers
        3. Remove extra whitespace
        """
        if pd.isna(text):
            return ""
        
        text = str(text).lower()
        # Remove numbers and special characters, keep only letters and spaces
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def tokenize_text(self, text):
        """
        Tokenize text into individual words.
        """
        tokens = word_tokenize(text)
        return tokens
    
    def remove_stopwords(self, tokens):
        """
        Remove common stopwords and non-informative words.
        """
        filtered_tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        return filtered_tokens
    
    def lemmatize_tokens(self, tokens):
        """
        Reduce words to their base form (lemma).
        """
        lemmatized = [self.lemmatizer.lemmatize(token) for token in tokens]
        return lemmatized
    
    def preprocess_text(self, text):
        """
        Full preprocessing pipeline for a single text.
        """
        cleaned = self.clean_text(text)
        tokens = self.tokenize_text(cleaned)
        tokens = self.remove_stopwords(tokens)
        tokens = self.lemmatize_tokens(tokens)
        return ' '.join(tokens)
    
    def preprocess_dataset(self, df, text_column='Symptoms'):
        """
        Apply full preprocessing to the entire dataset.
        
        Returns:
            DataFrame with preprocessed text and encoded labels
        """
        df_processed = df.copy()
        
        # Clean Symptoms column
        df_processed['Symptoms_Clean'] = df_processed[text_column].apply(self.preprocess_text)
        
        # Encode categorical labels
        df_processed['Disease_Encoded'] = self.label_encoder.fit_transform(df_processed['Disease'])
        df_processed['Severity_Encoded'] = df_processed['Severity'].map({'Mild': 0, 'Moderate': 1, 'Severe': 2})
        
        # Extract symptom count as feature
        df_processed['Symptom_Count'] = df_processed['Symptoms'].apply(lambda x: len(str(x).split(',')))
        
        # Extract severity keywords
        def extract_severity_keywords(text):
            severity_keywords = []
            text_lower = str(text).lower()
            if any(word in text_lower for word in ['severe', 'intense', 'extreme', 'worsening', 'persistent']):
                severity_keywords.append('high_severity')
            if any(word in text_lower for word in ['mild', 'slight', 'occasional']):
                severity_keywords.append('low_severity')
            return ' '.join(severity_keywords) if severity_keywords else 'normal_severity'
        
        df_processed['Severity_Keywords'] = df_processed['Symptoms'].apply(extract_severity_keywords)
        
        return df_processed
    
    def extract_features(self, df_processed, max_features=2000):
        """
        Extract TF-IDF features from preprocessed text.
        """
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=(1, 2),  # Unigrams and bigrams
            min_df=2,
            max_df=0.9
        )
        
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(df_processed['Symptoms_Clean'])
        
        # Convert to DataFrame for inspection
        feature_names = self.tfidf_vectorizer.get_feature_names_out()
        tfidf_df = pd.DataFrame(
            tfidf_matrix.toarray(),
            columns=[f'tfidf_{name}' for name in feature_names]
        )
        
        return tfidf_matrix, tfidf_df, feature_names
    
    def save_preprocessor(self, path='models/preprocessor.pkl'):
        """
        Save the preprocessor for later use.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump({
                'label_encoder': self.label_encoder,
                'tfidf_vectorizer': self.tfidf_vectorizer,
                'lemmatizer': self.lemmatizer,
                'stop_words': self.stop_words
            }, f)
        print(f"Preprocessor saved to {path}")
    
    def load_preprocessor(self, path='models/preprocessor.pkl'):
        """
        Load a saved preprocessor.
        """
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.label_encoder = data['label_encoder']
            self.tfidf_vectorizer = data['tfidf_vectorizer']
            self.lemmatizer = data['lemmatizer']
            self.stop_words = data['stop_words']
        print(f"Preprocessor loaded from {path}")


def main(ctx):
    """Main preprocessing pipeline."""
    run_dir = ctx['runDir']
    
    # Load raw data
    raw_path = os.path.join(run_dir, '..', 'smart-medical-assistant', 'data', 'raw', 'medical_dataset.csv')
    df = pd.read_csv(raw_path)
    
    print(f"Loaded {len(df)} records from raw dataset")
    
    # Initialize preprocessor
    preprocessor = MedicalDataPreprocessor()
    
    # Preprocess dataset
    df_processed = preprocessor.preprocess_dataset(df)
    
    # Extract TF-IDF features
    tfidf_matrix, tfidf_df, feature_names = preprocessor.extract_features(df_processed)
    
    # Save processed data
    processed_dir = os.path.join(run_dir, '..', 'smart-medical-assistant', 'data', 'processed')
    os.makedirs(processed_dir, exist_ok=True)
    
    df_processed.to_csv(os.path.join(processed_dir, 'medical_dataset_processed.csv'), index=False)
    tfidf_df.to_csv(os.path.join(processed_dir, 'tfidf_features.csv'), index=False)
    
    # Save preprocessor
    models_dir = os.path.join(run_dir, '..', 'smart-medical-assistant', 'models')
    os.makedirs(models_dir, exist_ok=True)
    preprocessor.save_preprocessor(os.path.join(models_dir, 'preprocessor.pkl'))
    
    # Save feature names
    with open(os.path.join(processed_dir, 'feature_names.txt'), 'w') as f:
        for name in feature_names:
            f.write(f"{name}\n")
    
    print(f"\nPreprocessing Complete!")
    print(f"Original features: {df.shape[1]}")
    print(f"Processed records: {len(df_processed)}")
    print(f"TF-IDF features: {len(feature_names)}")
    print(f"Disease classes: {len(preprocessor.label_encoder.classes_)}")
    print(f"Saved to: {processed_dir}")
    
    return {
        'records': len(df_processed),
        'tfidf_features': len(feature_names),
        'disease_classes': list(preprocessor.label_encoder.classes_)
    }
