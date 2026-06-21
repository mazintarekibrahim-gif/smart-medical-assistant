/**
 * Smart Medical Assistant — Frontend Application
 * Handles symptom analysis, API communication, and dynamic UI updates.
 */

(function () {
    'use strict';

    // ============================================
    // Configuration
    // ============================================

    const API_BASE_URL = 'http://localhost:5000';
    const API_ENDPOINT = '/api/analyze';

    // ============================================
    // DOM Elements
    // ============================================

    const form = document.getElementById('symptom-form');
    const symptomInput = document.getElementById('symptom-input');
    const submitBtn = document.getElementById('submit-btn');
    const exampleChips = document.querySelectorAll('.example-chip');
    const loadingState = document.getElementById('loading-state');
    const errorState = document.getElementById('error-state');
    const errorMessage = document.getElementById('error-message');
    const retryBtn = document.getElementById('retry-btn');
    const resultsSection = document.getElementById('results');
    const yearSpan = document.getElementById('year');

    // Result elements
    const extractedSymptomsContainer = document.getElementById('extracted-symptoms');
    const extractedSymptomsEmpty = document.getElementById('extracted-symptoms-empty');
    const topPredictionName = document.getElementById('top-prediction-name');
    const topConfidenceBar = document.getElementById('top-confidence-bar');
    const topConfidenceValue = document.getElementById('top-confidence-value');
    const predictionsList = document.getElementById('predictions-list');
    const treatmentList = document.getElementById('treatment-list');
    const treatmentEmpty = document.getElementById('treatment-empty');
    const precautionsList = document.getElementById('precautions-list');
    const precautionsEmpty = document.getElementById('precautions-empty');
    const urgencyAlert = document.getElementById('urgency-alert');
    const urgencyValue = document.getElementById('urgency-value');
    const urgencyAction = document.getElementById('urgency-action');
    const disclaimerText = document.getElementById('disclaimer-text');

    // ============================================
    // Utility Functions
    // ============================================

    /**
     * Set the copyright year dynamically.
     */
    function setYear() {
        if (yearSpan) {
            yearSpan.textContent = new Date().getFullYear().toString();
        }
    }

    /**
     * Scroll to an element smoothly.
     * @param {HTMLElement} element
     */
    function scrollToElement(element) {
        if (!element) return;
        const navHeight = document.querySelector('.navbar')?.offsetHeight || 64;
        const rect = element.getBoundingClientRect();
        const scrollTop = window.scrollY || window.pageYOffset;
        window.scrollTo({
            top: rect.top + scrollTop - navHeight - 16,
            behavior: 'smooth'
        });
    }

    /**
     * Show a specific section and hide others.
     */
    function showSection(section) {
        loadingState.classList.remove('active');
        loadingState.setAttribute('aria-hidden', 'true');
        errorState.classList.remove('active');
        errorState.setAttribute('aria-hidden', 'true');
        resultsSection.classList.remove('active');
        resultsSection.setAttribute('aria-hidden', 'true');

        if (section === 'loading') {
            loadingState.classList.add('active');
            loadingState.setAttribute('aria-hidden', 'false');
        } else if (section === 'error') {
            errorState.classList.add('active');
            errorState.setAttribute('aria-hidden', 'false');
        } else if (section === 'results') {
            resultsSection.classList.add('active');
            resultsSection.setAttribute('aria-hidden', 'false');
        }
    }

    /**
     * Set loading state on the submit button.
     * @param {boolean} isLoading
     */
    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        submitBtn.classList.toggle('loading', isLoading);
    }

    /**
     * Format a confidence value as a percentage string.
     * @param {number} value
     * @returns {string}
     */
    function formatConfidence(value) {
        if (typeof value === 'number') {
            return Math.round(value * 100) + '%';
        }
        return '0%';
    }

    /**
     * Map urgency level to display info.
     * @param {string} level
     * @returns {{class: string, label: string, action: string}}
     */
    function getUrgencyInfo(level) {
        const normalized = (level || '').toString().toLowerCase().trim();

        if (normalized === 'high' || normalized === 'emergency' || normalized === 'critical') {
            return {
                class: 'urgency-high',
                label: 'High - Seek Immediate Care',
                action: 'Please consult a healthcare professional immediately or visit the nearest emergency department.'
            };
        }
        if (normalized === 'medium' || normalized === 'moderate' || normalized === 'warning') {
            return {
                class: 'urgency-medium',
                label: 'Medium - Monitor Closely',
                action: 'Schedule an appointment with a healthcare provider within the next 24-48 hours.'
            };
        }
        return {
            class: 'urgency-low',
            label: 'Low - Self-Care May Suffice',
            action: 'Monitor your symptoms. If they worsen or persist, consult a healthcare provider.'
        };
    }

    // ============================================
    // Rendering Functions
    // ============================================

    /**
     * Render extracted symptoms as tags.
     * @param {string[]} symptoms
     */
    function renderExtractedSymptoms(symptoms) {
        extractedSymptomsContainer.innerHTML = '';

        if (!symptoms || symptoms.length === 0) {
            extractedSymptomsContainer.style.display = 'none';
            extractedSymptomsEmpty.style.display = 'block';
            return;
        }

        extractedSymptomsEmpty.style.display = 'none';
        extractedSymptomsContainer.style.display = 'flex';

        symptoms.forEach(symptom => {
            const tag = document.createElement('span');
            tag.className = 'symptom-tag';
            tag.textContent = symptom;
            extractedSymptomsContainer.appendChild(tag);
        });
    }

    /**
     * Render the top prediction with confidence bar.
     * @param {Object} prediction
     */
    function renderTopPrediction(prediction) {
        if (!prediction) {
            topPredictionName.textContent = 'No prediction available';
            topConfidenceBar.style.width = '0%';
            topConfidenceValue.textContent = '0%';
            return;
        }

        const diseaseName = prediction.disease || prediction.name || 'Unknown';
        const confidence = typeof prediction.confidence === 'number' ? prediction.confidence : 0;

        topPredictionName.textContent = diseaseName;
        topConfidenceValue.textContent = formatConfidence(confidence);

        // Animate the bar after a small delay for visual effect
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                topConfidenceBar.style.width = (confidence * 100) + '%';
            });
        });
    }

    /**
     * Render the list of top 5 predictions with confidence bars.
     * @param {Object[]} predictions
     */
    function renderPredictionsList(predictions) {
        predictionsList.innerHTML = '';

        if (!predictions || predictions.length === 0) {
            predictionsList.innerHTML = '<p class="empty-text">No predictions available.</p>';
            return;
        }

        // Take top 5
        const topFive = predictions.slice(0, 5);

        topFive.forEach((prediction, index) => {
            const diseaseName = prediction.disease || prediction.name || 'Unknown';
            const confidence = typeof prediction.confidence === 'number' ? prediction.confidence : 0;

            const item = document.createElement('div');
            item.className = 'prediction-item';
            item.innerHTML = `
                <span class="prediction-rank">${index + 1}</span>
                <div class="prediction-info">
                    <span class="prediction-disease">${escapeHtml(diseaseName)}</span>
                    <div class="prediction-bar-bg">
                        <div class="prediction-bar-fill" style="width: 0%"></div>
                    </div>
                </div>
                <span class="prediction-percent">${formatConfidence(confidence)}</span>
            `;
            predictionsList.appendChild(item);

            // Animate the bar
            const barFill = item.querySelector('.prediction-bar-fill');
            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    barFill.style.width = (confidence * 100) + '%';
                });
            });
        });
    }

    /**
     * Render a list of recommendations.
     * @param {HTMLElement} container
     * @param {HTMLElement} emptyEl
     * @param {string[]|string} items
     */
    function renderRecommendations(container, emptyEl, items) {
        container.innerHTML = '';

        let itemList = [];
        if (Array.isArray(items)) {
            itemList = items.filter(item => item && item.toString().trim());
        } else if (typeof items === 'string' && items.trim()) {
            itemList = items.split(/[.,;]/).map(s => s.trim()).filter(Boolean);
        }

        if (itemList.length === 0) {
            container.style.display = 'none';
            emptyEl.style.display = 'block';
            return;
        }

        emptyEl.style.display = 'none';
        container.style.display = 'flex';

        itemList.forEach(item => {
            const el = document.createElement('div');
            el.className = 'recommendation-item';
            el.textContent = item.toString();
            container.appendChild(el);
        });
    }

    /**
     * Render the urgency alert.
     * @param {string} level
     * @param {string} actionMessage
     */
    function renderUrgency(level, actionMessage) {
        const info = getUrgencyInfo(level);

        urgencyAlert.className = 'urgency-alert ' + info.class;
        urgencyValue.textContent = info.label;
        urgencyAction.textContent = actionMessage || info.action;
    }

    /**
     * Render the disclaimer.
     * @param {string} disclaimer
     */
    function renderDisclaimer(disclaimer) {
        if (disclaimer && disclaimer.trim()) {
            disclaimerText.textContent = disclaimer;
        }
    }

    /**
     * Escape HTML to prevent XSS.
     * @param {string} text
     * @returns {string}
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // ============================================
    // API Communication
    // ============================================

    /**
     * Send the symptom text to the backend API.
     * @param {string} text
     * @returns {Promise<Object>}
     */
    async function analyzeSymptoms(text) {
        const response = await fetch(API_BASE_URL + API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    }

    // ============================================
    // Event Handlers
    // ============================================

    /**
     * Handle form submission.
     * @param {Event} event
     */
    async function handleSubmit(event) {
        event.preventDefault();

        const text = symptomInput.value.trim();

        if (!text || text.length < 5) {
            symptomInput.focus();
            symptomInput.classList.add('invalid');
            setTimeout(() => symptomInput.classList.remove('invalid'), 2000);
            return;
        }

        setLoading(true);
        showSection('loading');

        try {
            const data = await analyzeSymptoms(text);

            if (!data || data.success === false) {
                throw new Error(data.message || 'Analysis failed. Please try again.');
            }

            // Render results
            renderExtractedSymptoms(data.extracted_symptoms || []);
            renderTopPrediction(data.top_prediction || (data.predictions && data.predictions[0]));
            renderPredictionsList(data.predictions || []);
            renderRecommendations(treatmentList, treatmentEmpty, data.treatment_recommendations || data.treatments || []);
            renderRecommendations(precautionsList, precautionsEmpty, data.precautions || []);
            renderUrgency(data.urgency_level, data.action_message);
            renderDisclaimer(data.disclaimer);

            showSection('results');
            scrollToElement(resultsSection);

        } catch (error) {
            console.error('Analysis error:', error);
            errorMessage.textContent = error.message || 'Unable to connect to the analysis server. Please ensure the backend is running on port 5000.';
            showSection('error');
            scrollToElement(errorState);
        } finally {
            setLoading(false);
        }
    }

    /**
     * Handle example chip clicks.
     * @param {Event} event
     */
    function handleExampleClick(event) {
        const chip = event.currentTarget;
        const symptoms = chip.dataset.symptoms;
        if (symptoms) {
            symptomInput.value = symptoms;
            symptomInput.focus();
            // Scroll to input on mobile
            if (window.innerWidth < 768) {
                scrollToElement(symptomInput);
            }
        }
    }

    /**
     * Handle retry button click.
     */
    function handleRetry() {
        errorState.classList.remove('active');
        errorState.setAttribute('aria-hidden', 'true');
        symptomInput.focus();
    }

    // ============================================
    // Initialization
    // ============================================

    function init() {
        setYear();

        // Event listeners
        form.addEventListener('submit', handleSubmit);
        retryBtn.addEventListener('click', handleRetry);

        exampleChips.forEach(chip => {
            chip.addEventListener('click', handleExampleClick);
        });

        // Add subtle entrance animation to the analyzer card
        const analyzerCard = document.querySelector('.analyzer-card');
        if (analyzerCard) {
            analyzerCard.style.opacity = '0';
            analyzerCard.style.transform = 'translateY(16px)';
            requestAnimationFrame(() => {
                analyzerCard.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                analyzerCard.style.opacity = '1';
                analyzerCard.style.transform = 'translateY(0)';
            });
        }
    }

    // Start when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
