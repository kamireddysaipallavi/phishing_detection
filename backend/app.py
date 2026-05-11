from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
import socket
import requests

app = Flask(__name__)
CORS(app)

# ================= LOAD MODELS =================
email_model = joblib.load("email_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
url_model = joblib.load("url_model.pkl")

# ================= DATA =================
known_brands = ["google","facebook","instagram","twitter","linkedin","amazon","paypal","apple","microsoft","netflix","youtube"]

suspicious_tlds = [".xyz",".tk",".ml",".ga",".cf",".gq",".top",".click",".link",".work"]

suspicious_keywords = ["login","verify","secure","account","update","bank","password","otp","confirm","reset"]

# ================= HELPERS =================
def get_domain(url):
    try:
        domain = url.lower().split("//")[-1].split("/")[0]
        return domain.replace("www.", "").strip()
    except:
        return ""

def is_url_alive(url):
    try:
        domain = get_domain(url)

        # DNS check
        socket.gethostbyname(domain)

        # HTTP check
        try:
            response = requests.get(url, timeout=5)
            return response.status_code < 400
        except:
            return False

    except:
        return False

# ================= URL CHECK =================
def check_url(url):
    features = []
    url_lower = url.lower()
    domain = get_domain(url)
    domain_base = domain.split(".")[0] if domain else ""

    is_phish = False
    confidence = 0.1

    # 1. IP Address
    if re.search(r'http[s]?://\d+\.\d+\.\d+\.\d+', url):
        features.append({
            "title": "IP Address Used",
            "description": "Legitimate websites rarely use raw IP addresses.",
            "level": "high"
        })
        return True, 0.99, features

    # 2. @ symbol
    if "@" in url:
        features.append({
            "title": "Suspicious '@' Symbol",
            "description": "URL contains '@' which hides real destination.",
            "level": "high"
        })
        is_phish = True

    # 3. Fake domain (brand impersonation)
    for brand in known_brands:
        if brand in url_lower and domain_base != brand:
            features.append({
                "title": "Fake Domain Detected",
                "description": f"This URL pretends to be {brand} but is not official.",
                "level": "high"
            })
            is_phish = True
            confidence = max(confidence, 0.95)

    # 4. Suspicious TLD
    if any(domain.endswith(tld) for tld in suspicious_tlds):
        features.append({
            "title": "Suspicious Domain Extension",
            "description": "Domain uses risky extension like .xyz, .tk.",
            "level": "medium"
        })
        is_phish = True

    # 5. Hyphens
    if domain_base.count("-") >= 2:
        features.append({
            "title": "Too Many Hyphens",
            "description": "Phishing URLs often contain multiple hyphens.",
            "level": "medium"
        })
        is_phish = True

    # 6. Long URL
    if len(url) > 100:
        features.append({
            "title": "Very Long URL",
            "description": "Long URLs may hide malicious intent.",
            "level": "medium"
        })
        is_phish = True

    # 7. Keywords
    if any(k in url_lower for k in suspicious_keywords):
        features.append({
            "title": "Suspicious Keywords",
            "description": "Contains words like login/verify/password.",
            "level": "medium"
        })
        is_phish = True

    # Safe case
    if not features:
        features.append({
            "title": "Legitimate Domain",
            "description": "No phishing indicators detected.",
            "level": "low"
        })

    return is_phish, confidence, features

# ================= EMAIL CHECK =================
def check_email(text):
    text_lower = text.lower()
    features = []

    if "urgent" in text_lower:
        features.append({
            "title": "Urgency Detected",
            "description": "Creates pressure to act quickly.",
            "level": "high"
        })

    if "otp" in text_lower or "password" in text_lower:
        features.append({
            "title": "Sensitive Info Request",
            "description": "Asks for OTP or password.",
            "level": "high"
        })

    if "click" in text_lower:
        features.append({
            "title": "Suspicious Link Request",
            "description": "Encourages clicking unknown links.",
            "level": "medium"
        })

    is_phish = len(features) > 0
    confidence = 0.9 if is_phish else 0.1

    if not features:
        features.append({
            "title": "Normal Message",
            "description": "No phishing language detected.",
            "level": "low"
        })

    return is_phish, confidence, features

# ================= ROUTES =================

@app.route('/url', methods=['POST'])
def analyze_url():
    data = request.json
    url = data['input']

    # Check if URL exists
    if not is_url_alive(url):
        return jsonify({
            "prediction": "Phishing",
            "confidence": 99,
            "features": [{
                "title": "Fake / Invalid Domain",
                "description": "This website does not exist or is unreachable.",
                "level": "high"
            }]
        })

    is_phish, confidence, features = check_url(url)

    return jsonify({
        "prediction": "Phishing" if is_phish else "Safe",
        "confidence": round(confidence * 100, 2),
        "features": features
    })


@app.route('/email', methods=['POST'])
def analyze_email():
    data = request.json
    text = data['input']

    is_phish, confidence, features = check_email(text)

    return jsonify({
        "prediction": "Phishing" if is_phish else "Safe",
        "confidence": round(confidence * 100, 2),
        "features": features
    })

# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)