## **AI-Powered Patient Triage Support System** 

## _**Innovating Healthcare with Artificial Intelligence**_ 

## **1. Project Overview** 

## Writing 

This project proposes the development of an AI-powered patient triage support system designed to assist healthcare professionals in accurately prioritizing patients based on urgency. The system leverages machine learning techniques to analyze patient symptoms, vital signs, and contextual factors, providing real-time triage recommendations, risk scores, and decision-support alerts. 

The goal is to reduce misclassification of critical patients, improve response time, and enhance clinical decision-making—especially in resource-limited healthcare settings where time and data constraints are significant. 

## **2. Problem Statement** 

## Writing 

Triage is a critical process in healthcare that determines the priority of patient care. However, in many healthcare facilities—especially in low-resource environments— triage decisions are made under pressure, often with incomplete or rapidly changing patient information. 

This can lead to underestimation of severe cases, delayed intervention, and preventable loss of life. Real-world experiences have shown that patients with hidden internal injuries or subtle symptoms may be incorrectly classified as non-urgent, leading to fatal outcomes. 

There is a need for an intelligent, reliable system that supports healthcare workers in making more accurate and consistent triage decisions, while accounting for uncertainty and data limitations. 

## **3. Objectives** 

## **General Objective** 

- To develop an AI-powered system that enhances accuracy and reliability in patient triage. 

## **Specific Objectives** 

- Predict patient urgency level (Emergency, Urgent, Non-Urgent) 

- Reduce risk of misclassification in triage decisions 

- Provide confidence-aware predictions and alerts 

- Improve decision-making speed in clinical environments 

- Ensure ethical and explainable AI usage 

## **4. Proposed Solution** 

Writing 

The proposed system is a web-based AI-powered triage assistant that takes patient data as input and generates real-time triage recommendations. The system integrates machine learning with rule-based clinical insights to produce interpretable and actionable outputs. 

It is designed as a decision-support tool that augments—not replaces—clinical judgment. By combining predictive modeling with confidence scoring and alert mechanisms, the system helps healthcare workers identify high-risk patients more reliably. 

## **5. System Features** 

## **Core Features** 

- Patient triage classification: 

   - Emergency 

   - Urgent 

   - Non-Urgent 

- Risk scoring system 

- Confidence level indicator 

## **Smart Alerts** 

- Low confidence warning 

- High-risk symptom detection 

- Possible misclassification alerts 

## **Explainability** 

- Feature importance display 

- Key contributing factors for each decision 

## **6. Dataset Strategy** 

Writing 

Due to the limited availability of standardized triage datasets, this project utilizes a hybrid data approach combining publicly available healthcare datasets and simulated triage labels. 

Data sources include physiological datasets containing vital signs (e.g., heart rate, respiratory rate, oxygen saturation) and symptom-based datasets. These datasets are integrated and enriched with simulated triage classifications based on clinical guidelines. 

Data preprocessing techniques such as handling missing values, encoding categorical variables, and balancing class distribution are applied to ensure data quality and model robustness. All data used is anonymized and complies with ethical standards. 

## **7. AI Approach** 

## **Model Type** 

- Supervised Machine Learning (Classification) 

## **Algorithm** 

- Random Forest Classifier 

## **Why Random Forest?** 

- Handles structured healthcare data effectively 

- Robust to noise and missing values 

- Provides feature importance (interpretability) 

- Fast and suitable for real-time applications 

## **Model Pipeline** 

- Data preprocessing 

- Feature engineering 

- Model training 

- Prediction + confidence scoring 

## **Evaluation Metrics** 

- Recall (priority for emergency cases) 

- Precision 

- F1-score 

- Confusion matrix 

## **8. System Architecture** 

## **Components** 

## 1. **User Interface** 

`o` Web-based input form for clinicians 

## 2. **Data Processing Layer** 

- Cleans and prepares input data 

## 3. **AI Model Layer** 

`o` Generates predictions and probabilities 

## 4. **Decision Support Layer** 

`o` Adds alerts, confidence, and explanations 

## 5. **Output Dashboard** 

`o` Displays triage results visually 

## **Data Flow** 

Input → Processing → Model → Decision Layer → Dashboard 

## **9. Deployment Strategy** 

- Web-based application (Streamlit / Flask) 

- Accessible on low-resource devices 

- Scalable for integration with hospital systems 

- Potential mobile deployment for rural clinics 

## **10. Ethical Considerations** 

## Writing 

This system is designed with a strong emphasis on ethical AI principles. It functions as a decision-support tool rather than a replacement for clinical judgment, ensuring that healthcare professionals remain in control of final decisions. 

The system incorporates explainability features to make predictions transparent and understandable. Confidence scores and uncertainty warnings are provided to prevent over-reliance on the model. 

All data used is anonymized and sourced from publicly available datasets, ensuring patient privacy and compliance with ethical standards. 

## **11. Expected Impact** 

- Improved triage accuracy 

- Reduced patient mortality due to misclassification 

- Faster clinical decision-making 

- Enhanced healthcare efficiency 

- Better support for healthcare workers in high-pressure environments 

## **12. Innovation & Uniqueness** 

- Combines **AI + decision support + confidence awareness** 

- Addresses **real-world triage failures** 

- Focuses on **data-limited environments** 

- Integrates **ethical AI principles (transparency + trust)** 

## **13. Conclusion** 

## Writing 

This project presents a practical and impactful application of artificial intelligence in healthcare. By addressing the critical challenge of triage misclassification, the system has the potential to improve patient outcomes and support healthcare professionals in making more informed decisions. 

With a focus on usability, ethical responsibility, and real-world applicability, this solution demonstrates how AI can be leveraged to create meaningful and life-saving innovations in healthcare. 

