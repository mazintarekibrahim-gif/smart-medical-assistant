"""
NLP Symptom Extractor Module
Smart Medical Assistant - Natural Language Processing Pipeline
"""

import re
import string
import numpy as np
from collections import OrderedDict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)


class SymptomExtractor:
    """
    NLP pipeline for extracting medical symptoms from natural language text.
    """
    
    # Comprehensive medical symptom dictionary
    MEDICAL_SYMPTOMS = {
        'fever': ['fever', 'high temperature', 'hot', 'burning up', 'temperature', 'febrile', 'pyrexia', 'hyperthermia'],
        'headache': ['headache', 'head pain', 'migraine', 'head ache', 'splitting headache', 'throbbing head', 'tension headache'],
        'cough': ['cough', 'coughing', 'hacking', 'wet cough', 'dry cough', 'persistent cough', 'coughing up', 'whooping'],
        'sore throat': ['sore throat', 'throat pain', 'painful throat', 'scratchy throat', 'throat irritation', 'strep throat', 'pharyngitis'],
        'runny nose': ['runny nose', 'runny nostrils', 'nasal discharge', 'dripping nose', 'rhinorrhea', 'runny nose', 'nasal drip'],
        'sneezing': ['sneezing', 'sneezes', 'sneezed', 'sternutation', 'sneeze attacks'],
        'congestion': ['congestion', 'stuffy nose', 'nasal congestion', 'blocked nose', 'sinus congestion', 'stuffy sinuses'],
        'body aches': ['body aches', 'body pain', 'aching body', 'muscle pain', 'muscle aches', 'myalgia', 'sore muscles', 'aching muscles', 'muscle soreness'],
        'fatigue': ['fatigue', 'tired', 'exhaustion', 'lethargy', 'weariness', 'lack of energy', 'no energy', 'tiredness', 'weakness', 'feeling drained', 'malaise'],
        'chills': ['chills', 'shivering', 'shaking', 'rigors', 'cold sweats', 'chilly', 'shivering'],
        'nausea': ['nausea', 'nauseated', 'feeling sick', 'queasy', 'upset stomach', 'stomach nausea', 'sick feeling'],
        'vomiting': ['vomiting', 'throwing up', 'puking', 'emesis', 'retching', 'vomited', 'regurgitation'],
        'diarrhea': ['diarrhea', 'loose stools', 'watery stools', 'frequent stools', 'loose bowel', 'runny stools', 'dysentery'],
        'constipation': ['constipation', 'hard stools', 'difficulty passing stool', 'infrequent bowel', 'straining', 'obstipation'],
        'chest pain': ['chest pain', 'chest tightness', 'pressure in chest', 'chest discomfort', 'angina', 'sternal pain', 'thoracic pain'],
        'shortness of breath': ['shortness of breath', 'breathing difficulty', 'difficulty breathing', 'dyspnea', 'cannot breathe', 'trouble breathing', 'wheezing breath', 'labored breathing', 'breathlessness'],
        'dizziness': ['dizziness', 'lightheaded', 'vertigo', 'spinning', 'unsteady', 'feeling faint', 'woozy', 'giddiness'],
        'loss of taste': ['loss of taste', 'no taste', 'tasteless', 'dysgeusia', 'cannot taste', 'altered taste', 'ageusia'],
        'loss of smell': ['loss of smell', 'no smell', 'anosmia', 'cannot smell', 'smell loss', 'hyposmia'],
        'abdominal pain': ['abdominal pain', 'stomach pain', 'belly pain', 'tummy ache', 'gastric pain', 'stomach ache', 'abdominal cramps', 'stomach cramps'],
        'rash': ['rash', 'skin rash', 'hives', 'urticaria', 'skin eruption', 'dermatitis', 'red skin', 'skin irritation'],
        'jaundice': ['jaundice', 'yellow skin', 'yellow eyes', 'yellowing', 'icterus', 'yellowish skin', 'yellow complexion'],
        'joint pain': ['joint pain', 'arthralgia', 'aching joints', 'painful joints', 'joint swelling', 'swollen joints', 'stiff joints'],
        'swelling': ['swelling', 'edema', 'puffy', 'bloating', 'swollen', 'water retention', 'fluid retention'],
        'weight loss': ['weight loss', 'losing weight', 'unexplained weight loss', 'rapid weight loss', 'sudden weight loss', 'wasting', 'cachexia'],
        'weight gain': ['weight gain', 'gaining weight', 'unexplained weight gain', 'sudden weight gain', 'increased weight'],
        'thirst': ['thirst', 'excessive thirst', 'very thirsty', 'polydipsia', 'dehydrated', 'always thirsty'],
        'frequent urination': ['frequent urination', 'urinating often', 'polyuria', 'peeing a lot', 'constant urination', 'urinary frequency'],
        'burning urination': ['burning urination', 'painful urination', 'dysuria', 'burning when peeing', 'stinging urine', 'urinary burning'],
        'blood in urine': ['blood in urine', 'hematuria', 'bloody urine', 'red urine', 'pink urine', 'urine with blood'],
        'blurred vision': ['blurred vision', 'blurry vision', 'vision problems', 'double vision', 'seeing blurry', 'visual disturbance', 'fuzzy vision'],
        'numbness': ['numbness', 'tingling', 'pins and needles', 'paresthesia', 'loss of sensation', 'numb', 'asleep feeling', 'tingling sensation'],
        'confusion': ['confusion', 'disoriented', 'mental fog', 'memory problems', 'confused', 'delirium', 'altered mental state', 'mental confusion'],
        'depression': ['depression', 'sadness', 'hopelessness', 'low mood', 'feeling down', 'melancholy', 'despair', 'depressed mood', 'persistent sadness'],
        'anxiety': ['anxiety', 'worry', 'nervousness', 'panic', 'fear', 'unease', 'apprehension', 'restlessness', 'anxious', 'feeling anxious'],
        'insomnia': ['insomnia', 'cannot sleep', 'sleep problems', 'sleeplessness', 'difficulty sleeping', 'poor sleep', 'sleep disturbance', 'waking up frequently'],
        'sweating': ['sweating', 'excessive sweating', 'night sweats', 'perspiration', 'hyperhidrosis', 'profuse sweating', 'drenched in sweat'],
        'appetite loss': ['appetite loss', 'loss of appetite', 'not hungry', 'anorexia', 'decreased appetite', 'no appetite', 'refusing food'],
        'heart palpitations': ['heart palpitations', 'racing heart', 'irregular heartbeat', 'fluttering', 'heart pounding', 'tachycardia', 'heart skipping beats'],
        'back pain': ['back pain', 'lower back pain', 'upper back pain', 'spinal pain', 'lumbar pain', 'back ache', 'back soreness', 'sciatica'],
        'stiffness': ['stiffness', 'joint stiffness', 'morning stiffness', 'rigid', 'tight muscles', 'reduced mobility', 'hard to move'],
        'wheezing': ['wheezing', 'wheezed', 'wheeze', 'noisy breathing', 'whistling sound', 'breathing sounds'],
        'chest tightness': ['chest tightness', 'chest pressure', 'constricted chest', 'chest heaviness', 'tight chest', 'chest constriction'],
        'sensitivity to light': ['sensitivity to light', 'photophobia', 'light hurts', 'bright light sensitivity', 'light intolerance'],
        'sensitivity to sound': ['sensitivity to sound', 'phonophobia', 'noise sensitivity', 'sounds hurt', 'noise intolerance', 'sound sensitivity'],
        'throbbing pain': ['throbbing pain', 'pulsating pain', 'throbbing headache', 'pounding pain', 'beating pain'],
        'visual aura': ['visual aura', 'seeing spots', 'flashing lights', 'zigzag lines', 'blind spots', 'visual disturbances', 'auras'],
        'nosebleeds': ['nosebleeds', 'nose bleeding', 'epistaxis', 'bloody nose', 'nose hemorrhage'],
        'flushing': ['flushing', 'red face', 'facial redness', 'hot flashes', 'blushing', 'skin redness', 'face feels hot'],
        'slow healing': ['slow healing', 'wounds not healing', 'poor wound healing', 'delayed healing', 'skin not healing'],
        'hair loss': ['hair loss', 'alopecia', 'thinning hair', 'losing hair', 'baldness', 'hair falling out', 'receding hairline'],
        'dry skin': ['dry skin', 'skin dryness', 'xerosis', 'flaky skin', 'rough skin', 'itchy dry skin', 'scaly skin'],
        'cold sensitivity': ['cold sensitivity', 'cold intolerance', 'always cold', 'feeling cold', 'cold extremities', 'cold hands', 'cold feet'],
        'heat sensitivity': ['heat sensitivity', 'heat intolerance', 'always hot', 'feeling hot', 'warm intolerance', 'sweating in heat'],
        'tremor': ['tremor', 'shaking', 'trembling', 'shaky hands', 'involuntary shaking', 'quivering', 'essential tremor'],
        'bulging eyes': ['bulging eyes', 'proptosis', 'eye bulging', 'prominent eyes', 'eyes sticking out', 'exophthalmos'],
        'difficulty concentrating': ['difficulty concentrating', 'cannot focus', 'brain fog', 'poor concentration', 'trouble focusing', 'attention problems', 'lack of focus'],
        'feelings of worthlessness': ['feelings of worthlessness', 'feeling worthless', 'self-loathing', 'guilt', 'inadequacy', 'self-criticism', 'shame'],
        'thoughts of death': ['thoughts of death', 'suicidal thoughts', 'wanting to die', 'death ideation', 'suicidal ideation', 'self-harm thoughts', 'ending it all'],
        'panic attacks': ['panic attacks', 'panic', 'sudden fear', 'terror', 'overwhelming anxiety', 'panic episodes', 'acute anxiety'],
        'irritability': ['irritability', 'easily annoyed', 'short temper', 'mood swings', 'agitation', 'frustration', 'angry easily'],
        'muscle tension': ['muscle tension', 'tense muscles', 'muscle tightness', 'muscle knots', 'tight muscles', 'muscle stiffness'],
        'sleep disturbances': ['sleep disturbances', 'sleeping problems', 'restless sleep', 'waking up early', 'waking up at night', 'broken sleep', 'non-restorative sleep']
    }
    
    # Severity keywords
    SEVERITY_KEYWORDS = {
        'mild': ['mild', 'slight', 'minor', 'a little', 'somewhat', 'not too bad', 'tolerable', 'bearable', 'light', 'slight', 'minimal'],
        'moderate': ['moderate', 'fairly', 'quite', 'rather', 'somewhat severe', 'uncomfortable', 'noticeable', 'significant', 'considerable'],
        'severe': ['severe', 'extreme', 'intense', 'excruciating', 'unbearable', 'terrible', 'awful', 'worst', 'agonizing', 'crippling', 'debilitating', 'incapacitating', 'worsening', 'persistent', 'constant', 'chronic']
    }
    
    # Duration keywords
    DURATION_KEYWORDS = {
        'acute': ['sudden', 'abrupt', 'recent', 'started today', 'just started', 'a few hours', 'since yesterday', 'last night', 'this morning'],
        'subacute': ['few days', 'couple days', 'three days', 'four days', 'last week', 'about a week', 'started recently'],
        'chronic': ['weeks', 'months', 'years', 'long time', 'chronic', 'ongoing', 'persistent', 'recurring', 'keep coming back', 'always have', 'for years']
    }
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
    
    def preprocess_input(self, text):
        """Clean and normalize user input text."""
        text = str(text).lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove punctuation but keep important characters
        text = text.translate(str.maketrans('', '', string.punctuation.replace('-', '')))
        return text
    
    def extract_symptoms(self, text):
        """
        Extract symptoms from natural language text.
        
        Returns:
            dict: {
                'extracted_symptoms': list of matched symptom names,
                'matched_phrases': list of original matched phrases,
                'confidence': float,
                'severity': str or None,
                'duration': str or None
            }
        """
        text = self.preprocess_input(text)
        tokens = word_tokenize(text)
        lemmatized = [self.lemmatizer.lemmatize(t) for t in tokens]
        text_bigrams = [' '.join(pair) for pair in zip(tokens, tokens[1:])]
        text_trigrams = [' '.join(triplet) for triplet in zip(tokens, tokens[1:], tokens[2:])]
        
        extracted = OrderedDict()
        matched_phrases = []
        
        for canonical_symptom, variations in self.MEDICAL_SYMPTOMS.items():
            for variant in variations:
                # Check for multi-word phrases first
                if ' ' in variant:
                    if variant in text:
                        if canonical_symptom not in extracted:
                            extracted[canonical_symptom] = len(variant)
                            matched_phrases.append(variant)
                # Check for single words
                elif variant in tokens or variant in lemmatized:
                    if canonical_symptom not in extracted:
                        extracted[canonical_symptom] = len(variant)
                        matched_phrases.append(variant)
        
        # Extract severity
        severity = None
        severity_score = 0
        for level, keywords in self.SEVERITY_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    severity = level
                    severity_score = max(severity_score, len(kw))
        
        # Extract duration
        duration = None
        for dur, keywords in self.DURATION_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    duration = dur
                    break
        
        # Calculate confidence based on number of symptoms and match quality
        num_symptoms = len(extracted)
        if num_symptoms >= 5:
            confidence = 0.95
        elif num_symptoms >= 3:
            confidence = 0.85
        elif num_symptoms >= 2:
            confidence = 0.70
        elif num_symptoms >= 1:
            confidence = 0.50
        else:
            confidence = 0.0
        
        # Adjust confidence based on severity keywords
        if severity and num_symptoms > 0:
            confidence = min(0.99, confidence + 0.05)
        
        return {
            'extracted_symptoms': list(extracted.keys()),
            'matched_phrases': matched_phrases,
            'confidence': round(confidence, 2),
            'severity': severity,
            'duration': duration,
            'symptom_count': num_symptoms
        }
    
    def format_for_model(self, extraction_result):
        """
        Format extracted symptoms into a string suitable for the ML model.
        """
        symptoms = extraction_result['extracted_symptoms']
        if not symptoms:
            return ""
        
        # Add severity modifier if present
        severity = extraction_result.get('severity')
        if severity == 'severe':
            formatted = [f"severe {s}" for s in symptoms]
        elif severity == 'mild':
            formatted = [f"mild {s}" for s in symptoms]
        else:
            formatted = symptoms
        
        return ', '.join(formatted)
    
    def analyze(self, text):
        """
        Full NLP analysis pipeline.
        
        Returns comprehensive analysis of the input text.
        """
        extraction = self.extract_symptoms(text)
        model_input = self.format_for_model(extraction)
        
        analysis = {
            'raw_input': text,
            'preprocessed': self.preprocess_input(text),
            'extraction': extraction,
            'model_input': model_input,
            'recommendation': self._generate_recommendation(extraction)
        }
        
        return analysis
    
    def _generate_recommendation(self, extraction):
        """Generate a recommendation based on extraction results."""
        num_symptoms = extraction['symptom_count']
        severity = extraction['severity']
        
        if num_symptoms == 0:
            return {
                'level': 'info',
                'message': 'No symptoms were recognized. Please describe your symptoms more clearly.',
                'action': 'Please try describing specific symptoms like "fever", "headache", or "cough".'
            }
        elif severity == 'severe':
            return {
                'level': 'urgent',
                'message': f'You described {num_symptoms} symptoms, some with severe intensity.',
                'action': 'This condition may require immediate medical attention. Please consult a doctor as soon as possible. Do not rely solely on this system.'
            }
        elif num_symptoms >= 5:
            return {
                'level': 'warning',
                'message': f'Multiple symptoms ({num_symptoms}) detected.',
                'action': 'Consider consulting a healthcare provider, especially if symptoms persist or worsen.'
            }
        else:
            return {
                'level': 'caution',
                'message': f'{num_symptoms} symptom(s) detected.',
                'action': 'Monitor your symptoms. If they worsen or new symptoms appear, consult a healthcare provider.'
            }


# Example usage
if __name__ == '__main__':
    extractor = SymptomExtractor()
    
    test_inputs = [
        "I have fever, headache and sore throat",
        "I've been feeling very tired and thirsty lately, and I urinate a lot",
        "severe chest pain and shortness of breath that started suddenly",
        "my joints are swollen and painful, especially in the morning",
        "I feel sad all the time and have no energy to do anything"
    ]
    
    print("=" * 70)
    print("NLP SYMPTOM EXTRACTION TESTS")
    print("=" * 70)
    
    for text in test_inputs:
        result = extractor.analyze(text)
        print(f"\nInput: \"{text}\"")
        print(f"Extracted Symptoms: {result['extraction']['extracted_symptoms']}")
        print(f"Confidence: {result['extraction']['confidence']}")
        print(f"Severity: {result['extraction']['severity']}")
        print(f"Duration: {result['extraction']['duration']}")
        print(f"Model Input: {result['model_input']}")
        print(f"Recommendation: {result['recommendation']['action']}")
        print("-" * 70)
