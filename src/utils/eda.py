"""
Exploratory Data Analysis (EDA) for Smart Medical Assistant
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os

# Set visualization style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def perform_eda(df, output_dir='reports/figures'):
    """
    Comprehensive EDA for medical dataset.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 70)
    print("EXPLORATORY DATA ANALYSIS - SMART MEDICAL ASSISTANT")
    print("=" * 70)
    
    # 1. Basic Dataset Information
    print("\n" + "=" * 70)
    print("1. DATASET OVERVIEW")
    print("=" * 70)
    print(f"Total Records: {len(df)}")
    print(f"Total Columns: {len(df.columns)}")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    print(f"\nColumn Types:\n{df.dtypes}")
    print(f"\nMissing Values:\n{df.isnull().sum()}")
    
    # 2. Disease Distribution
    print("\n" + "=" * 70)
    print("2. DISEASE DISTRIBUTION")
    print("=" * 70)
    disease_counts = df['Disease'].value_counts()
    print(disease_counts.to_string())
    
    fig, ax = plt.subplots(figsize=(14, 8))
    disease_counts.plot(kind='barh', ax=ax, color='steelblue')
    ax.set_title('Distribution of Diseases in Dataset', fontsize=14, fontweight='bold')
    ax.set_xlabel('Number of Records', fontsize=12)
    ax.set_ylabel('Disease', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'disease_distribution.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    # 3. Severity Distribution
    print("\n" + "=" * 70)
    print("3. SEVERITY DISTRIBUTION")
    print("=" * 70)
    severity_counts = df['Severity'].value_counts()
    print(severity_counts.to_string())
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Bar chart
    severity_counts.plot(kind='bar', ax=ax1, color=['#2ecc71', '#f39c12', '#e74c3c'])
    ax1.set_title('Severity Distribution', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Severity Level', fontsize=12)
    ax1.set_ylabel('Count', fontsize=12)
    ax1.tick_params(axis='x', rotation=0)
    
    # Pie chart
    ax2.pie(severity_counts.values, labels=severity_counts.index, autopct='%1.1f%%',
            colors=['#2ecc71', '#f39c12', '#e74c3c'], startangle=90)
    ax2.set_title('Severity Proportion', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'severity_distribution.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    # 4. Symptom Analysis
    print("\n" + "=" * 70)
    print("4. SYMPTOM ANALYSIS")
    print("=" * 70)
    
    all_symptoms = []
    for symptoms_text in df['Symptoms']:
        all_symptoms.extend([s.strip() for s in str(symptoms_text).split(',')])
    
    symptom_counter = Counter(all_symptoms)
    top_20_symptoms = symptom_counter.most_common(20)
    
    print(f"Total Unique Symptoms: {len(symptom_counter)}")
    print(f"\nTop 20 Most Common Symptoms:")
    for symptom, count in top_20_symptoms:
        print(f"  {symptom}: {count}")
    
    fig, ax = plt.subplots(figsize=(14, 8))
    symptoms, counts = zip(*top_20_symptoms)
    ax.barh(range(len(symptoms)), counts, color='coral')
    ax.set_yticks(range(len(symptoms)))
    ax.set_yticklabels(symptoms)
    ax.invert_yaxis()
    ax.set_title('Top 20 Most Common Symptoms', fontsize=14, fontweight='bold')
    ax.set_xlabel('Frequency', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'top_symptoms.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    # 5. Symptom Count per Disease
    print("\n" + "=" * 70)
    print("5. SYMPTOM COUNT PER DISEASE")
    print("=" * 70)
    df['symptom_count'] = df['Symptoms'].apply(lambda x: len(str(x).split(',')))
    symptom_stats = df.groupby('Disease')['symptom_count'].agg(['mean', 'min', 'max']).round(2)
    print(symptom_stats.to_string())
    
    fig, ax = plt.subplots(figsize=(14, 8))
    symptom_stats['mean'].sort_values(ascending=True).plot(kind='barh', ax=ax, color='teal')
    ax.set_title('Average Symptom Count per Disease', fontsize=14, fontweight='bold')
    ax.set_xlabel('Average Number of Symptoms', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'symptom_count_per_disease.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    # 6. Severity by Disease
    print("\n" + "=" * 70)
    print("6. SEVERITY BY DISEASE")
    print("=" * 70)
    severity_by_disease = pd.crosstab(df['Disease'], df['Severity'], normalize='index') * 100
    print(severity_by_disease.round(1).to_string())
    
    fig, ax = plt.subplots(figsize=(14, 10))
    severity_by_disease.plot(kind='barh', stacked=True, ax=ax, 
                             color=['#2ecc71', '#f39c12', '#e74c3c'])
    ax.set_title('Severity Distribution by Disease (%)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Percentage', fontsize=12)
    ax.legend(title='Severity', loc='lower right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'severity_by_disease.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    # 7. Correlation Analysis (Symptom-Disease Matrix)
    print("\n" + "=" * 70)
    print("7. SYMPTOM-DISEASE CORRELATION")
    print("=" * 70)
    
    # Create symptom presence matrix
    top_symptoms = [s[0] for s in symptom_counter.most_common(15)]
    diseases = df['Disease'].unique()
    
    correlation_matrix = pd.DataFrame(0, index=diseases, columns=top_symptoms)
    
    for _, row in df.iterrows():
        disease = row['Disease']
        symptoms = [s.strip() for s in str(row['Symptoms']).split(',')]
        for symptom in symptoms:
            if symptom in top_symptoms:
                correlation_matrix.loc[disease, symptom] += 1
    
    # Normalize
    correlation_matrix = correlation_matrix.div(correlation_matrix.sum(axis=1), axis=0)
    
    fig, ax = plt.subplots(figsize=(14, 12))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='YlOrRd', 
                ax=ax, linewidths=0.5)
    ax.set_title('Symptom-Disease Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'symptom_disease_correlation.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    # 8. Word Cloud Alternative - Top symptom words
    print("\n" + "=" * 70)
    print("8. DESCRIPTIVE STATISTICS")
    print("=" * 70)
    print(df.describe(include='all').to_string())
    
    # 9. Summary Statistics
    print("\n" + "=" * 70)
    print("9. DATA QUALITY SUMMARY")
    print("=" * 70)
    print(f"✓ No missing values: {df.isnull().sum().sum() == 0}")
    print(f"✓ Dataset balanced: {disease_counts.min() / disease_counts.max() > 0.5}")
    print(f"✓ Symptom diversity: {len(symptom_counter)} unique symptoms")
    print(f"✓ Severity coverage: {df['Severity'].nunique()} levels")
    
    print(f"\n{'=' * 70}")
    print(f"EDA Complete. All figures saved to: {output_dir}")
    print(f"{'=' * 70}")
    
    return {
        'total_records': len(df),
        'unique_diseases': df['Disease'].nunique(),
        'unique_symptoms': len(symptom_counter),
        'top_symptoms': top_20_symptoms[:5],
        'figures_saved': 6
    }


def main(ctx):
    """Main EDA function."""
    run_dir = ctx['runDir']
    
    # Load data
    data_path = os.path.join(run_dir, '..', 'smart-medical-assistant', 'data', 'raw', 'medical_dataset.csv')
    df = pd.read_csv(data_path)
    
    # Output directory
    output_dir = os.path.join(run_dir, '..', 'smart-medical-assistant', 'reports', 'figures')
    
    result = perform_eda(df, output_dir)
    return result
