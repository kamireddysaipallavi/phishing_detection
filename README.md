# 🛡️ TRUSTA – ML based Phishing Detection System

TRUSTA is a smart cybersecurity web application designed to detect phishing attacks in URLs, Emails, and SMS messages using Machine Learning and Explainable AI concepts.

The system helps users identify malicious content through detailed analysis, confidence scores, and human-readable explanations.

---

## 🚀 Features

### 🔗 URL Phishing Detection
- Detects suspicious and fake URLs
- Identifies:
  - Fake domains
  - Suspicious keywords
  - IP-based URLs
  - Risky TLDs
  - Long or obfuscated URLs
- Provides explainable AI-based reasoning

### 📧 Email Phishing Detection
- Analyzes email content for phishing indicators
- Detects:
  - Urgency/scam language
  - Credential harvesting attempts
  - Suspicious wording
- Generates detailed explanations

### 📱 SMS Phishing (Smishing) Detection
- Detects fraudulent SMS messages
- Identifies OTP scams, fake bank alerts, prize scams, etc.
- Provides actionable safety recommendations

### 📊 User Dashboard
- Personalized user dashboard
- Tracks:
  - Total analyses
  - URL checks
  - Email checks
  - Threats detected
- Displays recent activity for each user separately

### 🌗 Dark / Light Theme
- Theme toggle support
- Modern cybersecurity-themed UI

### 🧠 Explainable AI Result Page
- Displays:
  - Prediction
  - Confidence score
  - Threat explanations
  - AI insights

---

## 🛠️ Technologies Used

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn
- TF-IDF Vectorizer
- Logistic Regression
- Random Forest

### Dataset
- Phishing URLs Dataset
- Enron Spam Dataset
- Custom phishing SMS patterns

---

## 📂 Project Structure

```bash
TRUSTA/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── url.html
│   ├── email.html
│   ├── sms.html
│   ├── result.html
│   └── dashboard.html
│
├── models/
│   ├── phishing_model.pkl
│   ├── vectorizer.pkl
│
├── app.py
├── requirements.txt
└── README.md
