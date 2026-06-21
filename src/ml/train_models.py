"""
Machine Learning Model Training & Evaluation
Smart Medical Assistant - Disease Classification Models
"""

import pandas as pd
import numpy as np
import os
import sys
import pickle
import time
import json
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
from preprocessing import MedicalDataPreprocessor


class MedicalMLTrainer:
    """
    Comprehensive ML training pipeline for disease classification.
    """
    
    def __init__(self, data_path='data/raw/medical_dataset.csv', output_dir='models'):
        self.data_path = data_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.models = {}
        self.results = {}
        self.preprocessor = MedicalDataPreprocessor()
        self.scaler = StandardScaler()
        
    def load_and_prepare_data(self):
        """Load and preprocess dataset."""
        print("Loading and preprocessing data...")
        df = pd.read_csv(self.data_path)
        
        # Preprocess
        df_processed = self.preprocessor.preprocess_dataset(df)
        
        # Extract features
        X_tfidf, tfidf_df, feature_names = self.preprocessor.extract_features(df_processed)
        
        # Labels
        y = df_processed['Disease_Encoded'].values
        y_disease = df_processed['Disease'].values
        
        # Additional features: symptom count, severity
        extra_features = df_processed[['Symptom_Count', 'Severity_Encoded']].values
        
        # Combine TF-IDF with extra features
        X_combined = np.hstack([X_tfidf.toarray(), extra_features])
        
        # Split data
        X_train, X_test, y_train, y_test, y_train_disease, y_test_disease = train_test_split(
            X_combined, y, y_disease, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features (important for SVM, Logistic Regression)
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.X_train, self.X_test = X_train, X_test
        self.X_train_scaled, self.X_test_scaled = X_train_scaled, X_test_scaled
        self.y_train, self.y_test = y_train, y_test
        self.y_train_disease, self.y_test_disease = y_train_disease, y_test_disease
        self.disease_classes = self.preprocessor.label_encoder.classes_
        
        print(f"Training samples: {len(X_train)}")
        print(f"Testing samples: {len(X_test)}")
        print(f"Features: {X_train.shape[1]}")
        print(f"Classes: {len(self.disease_classes)}")
        
        return self
    
    def train_logistic_regression(self):
        """Train Logistic Regression with hyperparameter tuning."""
        print("\n" + "="*60)
        print("Training Logistic Regression...")
        print("="*60)
        
        param_grid = {
            'C': [0.1, 1, 10, 100],
            'penalty': ['l2'],
            'solver': ['lbfgs', 'liblinear'],
            'max_iter': [1000]
        }
        
        model = LogisticRegression(random_state=42, class_weight='balanced')
        grid_search = GridSearchCV(
            model, param_grid, cv=5, scoring='f1_weighted', n_jobs=-1, verbose=0
        )
        grid_search.fit(self.X_train_scaled, self.y_train)
        
        best_model = grid_search.best_estimator_
        self.models['LogisticRegression'] = best_model
        
        print(f"Best Parameters: {grid_search.best_params_}")
        print(f"Best CV Score: {grid_search.best_score_:.4f}")
        
        return self._evaluate_model('LogisticRegression', best_model, self.X_test_scaled)
    
    def train_random_forest(self):
        """Train Random Forest with hyperparameter tuning."""
        print("\n" + "="*60)
        print("Training Random Forest...")
        print("="*60)
        
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5],
            'class_weight': ['balanced']
        }
        
        model = RandomForestClassifier(random_state=42)
        grid_search = GridSearchCV(
            model, param_grid, cv=5, scoring='f1_weighted', n_jobs=-1, verbose=0
        )
        grid_search.fit(self.X_train, self.y_train)
        
        best_model = grid_search.best_estimator_
        self.models['RandomForest'] = best_model
        
        print(f"Best Parameters: {grid_search.best_params_}")
        print(f"Best CV Score: {grid_search.best_score_:.4f}")
        
        return self._evaluate_model('RandomForest', best_model, self.X_test)
    
    def train_decision_tree(self):
        """Train Decision Tree with hyperparameter tuning."""
        print("\n" + "="*60)
        print("Training Decision Tree...")
        print("="*60)
        
        param_grid = {
            'max_depth': [10, 20, 30, None],
            'min_samples_split': [2, 5, 10],
            'criterion': ['gini', 'entropy'],
            'class_weight': ['balanced']
        }
        
        model = DecisionTreeClassifier(random_state=42)
        grid_search = GridSearchCV(
            model, param_grid, cv=5, scoring='f1_weighted', n_jobs=-1, verbose=0
        )
        grid_search.fit(self.X_train, self.y_train)
        
        best_model = grid_search.best_estimator_
        self.models['DecisionTree'] = best_model
        
        print(f"Best Parameters: {grid_search.best_params_}")
        print(f"Best CV Score: {grid_search.best_score_:.4f}")
        
        return self._evaluate_model('DecisionTree', best_model, self.X_test)
    
    def train_svm(self):
        """Train Support Vector Machine with hyperparameter tuning."""
        print("\n" + "="*60)
        print("Training SVM...")
        print("="*60)
        
        param_grid = {
            'C': [0.1, 1, 10],
            'kernel': ['linear', 'rbf'],
            'gamma': ['scale', 'auto']
        }
        
        model = SVC(random_state=42, class_weight='balanced', probability=True)
        grid_search = GridSearchCV(
            model, param_grid, cv=5, scoring='f1_weighted', n_jobs=-1, verbose=0
        )
        grid_search.fit(self.X_train_scaled, self.y_train)
        
        best_model = grid_search.best_estimator_
        self.models['SVM'] = best_model
        
        print(f"Best Parameters: {grid_search.best_params_}")
        print(f"Best CV Score: {grid_search.best_score_:.4f}")
        
        return self._evaluate_model('SVM', best_model, self.X_test_scaled)
    
    def train_naive_bayes(self):
        """Train Naive Bayes classifier."""
        print("\n" + "="*60)
        print("Training Naive Bayes...")
        print("="*60)
        
        # Use non-negative features for NB (after scaling some may be negative)
        X_train_nb = np.abs(self.X_train_scaled)
        X_test_nb = np.abs(self.X_test_scaled)
        
        model = MultinomialNB()
        model.fit(X_train_nb, self.y_train)
        self.models['NaiveBayes'] = model
        
        return self._evaluate_model('NaiveBayes', model, X_test_nb)
    
    def train_xgboost(self):
        """Train XGBoost classifier with hyperparameter tuning."""
        print("\n" + "="*60)
        print("Training XGBoost...")
        print("="*60)
        
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [3, 6, 9],
            'learning_rate': [0.01, 0.1, 0.3],
            'subsample': [0.8, 1.0]
        }
        
        model = xgb.XGBClassifier(
            random_state=42, 
            eval_metric='mlogloss',
            use_label_encoder=False
        )
        grid_search = GridSearchCV(
            model, param_grid, cv=5, scoring='f1_weighted', n_jobs=-1, verbose=0
        )
        grid_search.fit(self.X_train, self.y_train)
        
        best_model = grid_search.best_estimator_
        self.models['XGBoost'] = best_model
        
        print(f"Best Parameters: {grid_search.best_params_}")
        print(f"Best CV Score: {grid_search.best_score_:.4f}")
        
        return self._evaluate_model('XGBoost', best_model, self.X_test)
    
    def _evaluate_model(self, model_name, model, X_test):
        """Evaluate a trained model."""
        start_time = time.time()
        y_pred = model.predict(X_test)
        inference_time = time.time() - start_time
        
        # Calculate metrics
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(self.y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(self.y_test, y_pred, average='weighted', zero_division=0)
        
        # Cross-validation
        if model_name in ['LogisticRegression', 'SVM', 'NaiveBayes']:
            cv_scores = cross_val_score(model, self.X_train_scaled, self.y_train, cv=5, scoring='f1_weighted')
        else:
            cv_scores = cross_val_score(model, self.X_train, self.y_train, cv=5, scoring='f1_weighted')
        
        self.results[model_name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'inference_time': inference_time,
            'predictions': y_pred
        }
        
        print(f"Accuracy:  {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1 Score:  {f1:.4f}")
        print(f"CV Mean:   {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")
        print(f"Inference Time: {inference_time:.4f}s")
        
        return self
    
    def generate_comparison_report(self, output_dir='reports'):
        """Generate comparison report and visualizations."""
        os.makedirs(output_dir, exist_ok=True)
        
        print("\n" + "="*60)
        print("MODEL COMPARISON REPORT")
        print("="*60)
        
        # Create comparison DataFrame
        comparison_data = []
        for model_name, metrics in self.results.items():
            comparison_data.append({
                'Model': model_name,
                'Accuracy': metrics['accuracy'],
                'Precision': metrics['precision'],
                'Recall': metrics['recall'],
                'F1 Score': metrics['f1_score'],
                'CV Mean': metrics['cv_mean'],
                'CV Std': metrics['cv_std'],
                'Inference Time (s)': metrics['inference_time']
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_df = comparison_df.sort_values('F1 Score', ascending=False)
        
        print("\n" + comparison_df.to_string(index=False))
        
        # Save comparison table
        comparison_df.to_csv(os.path.join(output_dir, 'model_comparison.csv'), index=False)
        
        # Visualization 1: Metrics Comparison Bar Chart
        fig, ax = plt.subplots(figsize=(12, 6))
        x = np.arange(len(comparison_df))
        width = 0.15
        
        ax.bar(x - 2*width, comparison_df['Accuracy'], width, label='Accuracy', color='#3498db')
        ax.bar(x - width, comparison_df['Precision'], width, label='Precision', color='#2ecc71')
        ax.bar(x, comparison_df['Recall'], width, label='Recall', color='#f39c12')
        ax.bar(x + width, comparison_df['F1 Score'], width, label='F1 Score', color='#e74c3c')
        ax.bar(x + 2*width, comparison_df['CV Mean'], width, label='CV Mean', color='#9b59b6')
        
        ax.set_xlabel('Model', fontsize=12)
        ax.set_ylabel('Score', fontsize=12)
        ax.set_title('Model Performance Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(comparison_df['Model'], rotation=45, ha='right')
        ax.legend(loc='lower right')
        ax.set_ylim(0, 1.1)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'model_comparison.png'), dpi=150, bbox_inches='tight')
        plt.close()
        
        # Visualization 2: Confusion Matrix for Best Model
        best_model_name = comparison_df.iloc[0]['Model']
        best_predictions = self.results[best_model_name]['predictions']
        
        fig, ax = plt.subplots(figsize=(16, 14))
        cm = confusion_matrix(self.y_test, best_predictions)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                   xticklabels=self.disease_classes, yticklabels=self.disease_classes,
                   linewidths=0.5, cbar_kws={'label': 'Count'})
        ax.set_title(f'Confusion Matrix - {best_model_name} (Best Model)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Predicted Disease', fontsize=12)
        ax.set_ylabel('True Disease', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'confusion_matrix_{best_model_name}.png'), dpi=150, bbox_inches='tight')
        plt.close()
        
        # Save best model
        best_model = self.models[best_model_name]
        with open(os.path.join(self.output_dir, 'best_model.pkl'), 'wb') as f:
            pickle.dump(best_model, f)
        
        with open(os.path.join(self.output_dir, 'scaler.pkl'), 'wb') as f:
            pickle.dump(self.scaler, f)
        
        # Save results JSON
        with open(os.path.join(output_dir, 'model_results.json'), 'w') as f:
            json.dump({k: {kk: float(vv) if isinstance(vv, (np.floating, np.integer)) else vv 
                          for kk, vv in v.items() if kk != 'predictions'} 
                      for k, v in self.results.items()}, f, indent=2)
        
        print(f"\nBest Model: {best_model_name}")
        print(f"Best Model saved to: {self.output_dir}/best_model.pkl")
        print(f"All visualizations saved to: {output_dir}")
        
        return comparison_df
    
    def train_all_models(self):
        """Train all models and generate reports."""
        self.load_and_prepare_data()
        
        self.train_logistic_regression()
        self.train_random_forest()
        self.train_decision_tree()
        self.train_svm()
        self.train_naive_bayes()
        self.train_xgboost()
        
        comparison_df = self.generate_comparison_report()
        
        return comparison_df


def main(ctx):
    """Main training pipeline."""
    run_dir = ctx['runDir']
    
    # Paths
    data_path = os.path.join(run_dir, '..', 'smart-medical-assistant', 'data', 'raw', 'medical_dataset.csv')
    models_dir = os.path.join(run_dir, '..', 'smart-medical-assistant', 'models')
    reports_dir = os.path.join(run_dir, '..', 'smart-medical-assistant', 'reports')
    
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    
    # Initialize trainer
    trainer = MedicalMLTrainer(data_path=data_path, output_dir=models_dir)
    
    # Train all models
    comparison_df = trainer.train_all_models()
    
    return {
        'best_model': comparison_df.iloc[0]['Model'],
        'best_f1': float(comparison_df.iloc[0]['F1 Score']),
        'all_models': comparison_df.to_dict('records')
    }
