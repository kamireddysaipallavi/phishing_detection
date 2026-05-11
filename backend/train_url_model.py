import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

print("STARTED URL MODEL")

# Dummy dataset (simple rules)
data = [
    ["http://secure-bank.com", 0],
    ["https://google.com", 0],
    ["http://login-bank.xyz", 1],
    ["http://verify-account-now.com", 1],
    ["https://amazon.in", 0],
    ["http://free-money-win.com", 1]
]

df = pd.DataFrame(data, columns=["url", "label"])

# Feature extraction
def extract_features(url):
    return [
        len(url),
        url.count('.'),
        1 if "https" in url else 0,
        int(any(c.isdigit() for c in url)),
        int("@" in url)
    ]

X = df["url"].apply(extract_features).tolist()
y = df["label"]

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save
joblib.dump(model, "url_model.pkl")

print("URL model saved ✅")