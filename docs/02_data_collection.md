# Data Collection
## Chapter 2: Dataset Documentation

---

### 2.1 Data Source

The medical dataset was constructed through a **synthetic data generation approach** combined with medical knowledge from authoritative sources:

1. **Primary Sources:**
   - Mayo Clinic Symptom Database (reference only)
   - CDC (Centers for Disease Control and Prevention) Disease Guidelines
   - WHO Disease Classification (ICD-10 reference)
   - MedlinePlus Medical Encyclopedia

2. **Data Synthesis Method:**
   - Medical knowledge was extracted and structured
   - Synthetic patient records were generated based on established symptom-disease relationships
   - Severity levels were assigned based on medical literature
   - Treatment recommendations follow standard medical guidelines

3. **Dataset Version:** v1.0

### 2.2 Dataset Size

| Metric | Value |
|--------|-------|
| Total Records | 1,320 |
| Unique Diseases | 30 |
| Unique Symptoms | 120+ |
| Columns | 6 |
| File Size | ~180 KB |
| Languages | English |
| Date Created | 2024 |

### 2.3 Data Collection Methodology

1. **Disease Selection:**
   - Selected 30 common diseases affecting general population
   - Included both acute and chronic conditions
   - Covered multiple body systems (respiratory, cardiovascular, digestive, etc.)

2. **Symptom Mapping:**
   - Each disease mapped to 3-8 primary symptoms
   - Symptom frequency and co-occurrence patterns based on medical prevalence
   - Added symptom severity levels (mild, moderate, severe)

3. **Synthetic Generation:**
   - Generated 30-50 records per disease
   - Introduced realistic symptom variations (not all patients show all symptoms)
   - Added symptom severity variations (mild fever vs high fever)

### 2.4 Data Limitations

1. **Synthetic Nature:**
   - Data is synthetically generated, not from real patient records
   - May not capture all real-world symptom variations
   - No patient demographic data (age, gender, location)

2. **Scope Limitations:**
   - Limited to 30 diseases (common conditions only)
   - No rare diseases included
   - No comorbidity information (single disease per record)

3. **Medical Accuracy:**
   - Based on general medical knowledge
   - Not validated by medical professionals
   - Should NOT be used for actual diagnosis

4. **Language:**
   - English only (Arabic support planned for future)

### 2.5 Data Quality Metrics

| Metric | Value |
|--------|-------|
| Missing Values | 0% |
| Duplicate Records | 0% |
| Symptom Coverage | 120+ unique symptoms |
| Disease Balance | Relatively balanced across 30 classes |
| Text Quality | Clean, standardized English |

### 2.6 Ethical Considerations

- Dataset is for educational and research purposes only
- Not suitable for clinical decision-making
- Synthetic data avoids real patient privacy concerns
- Clear disclaimers included in system documentation

---

## Dataset Schema

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| Disease | Categorical | Disease name (30 unique values) | "Flu", "Diabetes" |
| Symptoms | Text | Comma-separated symptoms | "fever, headache, sore throat" |
| Severity | Categorical | Overall severity level | "Mild", "Moderate", "Severe" |
| Recommended_Treatment | Text | Suggested treatment approach | "Rest, fluids, acetaminophen" |
| Precautions | Text | Recommended precautions | "Stay hydrated, isolate if contagious" |
| Description | Text | Brief disease description | "Viral respiratory infection..." |

### 2.7 Disease Categories

1. Common Cold
2. Flu (Influenza)
3. COVID-19
4. Diabetes
5. Hypertension
6. Migraine
7. Asthma
8. Bronchitis
9. Pneumonia
10. Tuberculosis
11. Malaria
12. Dengue
13. Typhoid
14. Hepatitis A
15. Hepatitis B
16. Hepatitis C
17. Jaundice
18. Gastroenteritis
19. Food Poisoning
20. Appendicitis
21. Urinary Tract Infection (UTI)
22. Kidney Stones
23. Gallstones
24. Arthritis
25. Osteoporosis
26. Anemia
27. Hypothyroidism
28. Hyperthyroidism
29. Depression
30. Anxiety Disorder

---

*Note: This dataset is intended for educational purposes in a graduation project. It should not be used for actual medical diagnosis or treatment decisions.*
